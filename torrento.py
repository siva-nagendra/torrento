"""
Torrent Downloader using PySide6 and aria2c.
"""

import os
import re
import sys
import logging
import subprocess
from typing import List
from PySide6.QtCore import Signal, QThread
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QCheckBox,
    QTextEdit,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QSizePolicy,
    QFileDialog,
    QSpacerItem,
    QProgressBar,
    QApplication,
)


logging.basicConfig(level=logging.DEBUG)

DOWNLOADS_DIR = os.path.expanduser("~/Downloads")


class DownloadThread(QThread):
    """Thread to handle the download process."""

    progress_update = Signal(int)
    log_message = Signal(str)
    download_complete = Signal()  # Signal for download completion

    def __init__(self, args: List[str]) -> None:
        """Initialize the DownloadThread with the necessary arguments for aria2c."""
        super().__init__()
        self.args = args
        self.process = None  # Store the process object

    def run(self) -> None:
        """Run the download process."""
        with subprocess.Popen(
            self.args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True,
        ) as self.process:
            while True:
                line = self.process.stdout.readline()
                if not line:
                    break
                self.log_message.emit(line)  # Emit log message signal
                if "Download of selected files was complete" in line:
                    self.download_complete.emit()  # Emit download complete signal
                progress = re.search(r"\((\d+)%\)", line)
                if progress:
                    progress_value = int(progress.group(1))
                    self.progress_update.emit(progress_value)

    def stop(self) -> None:
        """Terminate the aria2c process if it's still running."""
        if (
            self.process and self.process.poll() is None
        ):  # Check if process is still running
            self.process.terminate()


class TorrentDownloader(QWidget):  # pylint: disable=too-many-instance-attributes
    """Widget to handle the torrent downloading UI and functionality."""

    def __init__(self) -> None:
        """Initialize the Torrent Downloader Widget."""
        super().__init__()
        self.torrent_path = None
        self.torrent_name = "Torrent Downloader"
        self.download_thread = None
        self.init_ui()

    def init_ui(self) -> None:
        """Initialize the UI components."""
        self.setWindowTitle(self.torrent_name)
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # New Load Torrent File Button and Label
        self.load_torrent_button = QPushButton("Load Torrent")
        self.load_torrent_button.setMaximumWidth(100)
        self.load_torrent_button.clicked.connect(self.load_torrent_file)
        self.file_info_layout = QHBoxLayout()
        self.file_info_layout.addWidget(self.load_torrent_button)

        self.download_location_layout = QHBoxLayout()
        self.download_location_label = QLabel("Download Location:")
        self.download_location_textbox = QLineEdit(DOWNLOADS_DIR)

        self.download_location_layout.addWidget(self.download_location_label)
        self.download_location_layout.addWidget(self.download_location_textbox)

        spacer = QSpacerItem(
            20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed
        )  # Adjust the height value to 10

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        self.list_widget.setStyleSheet(
            """
            QListWidget::item {
                border-bottom: 1px solid #353535;
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #043757;
            }
        """
        )

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.handle_download)

        # Create a horizontal layout for the progress components
        self.progress_layout = QHBoxLayout()

        # Create and add the Progress label, ProgressBar,
        # and Progress Percentage label to the horizontal layout
        self.progress_label = QLabel("Progress:")
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
                height: 20px;
            }

            QProgressBar::chunk {
                background-color: #043757;
                width: 10px;  /* makes it a dashed progress bar */
            }
        """
        )

        # Create the checkbox
        self.more_info_checkbox = QCheckBox("More info")
        self.more_info_checkbox.setChecked(True)
        self.more_info_checkbox.stateChanged.connect(self.toggle_log_visibility)

        self.progress_layout.addWidget(self.progress_label)
        self.progress_layout.addWidget(self.progress_bar)
        self.progress_layout.addWidget(self.more_info_checkbox)

        self.log_widget = QTextEdit()
        self.log_widget.setReadOnly(True)
        self.log_widget.setFixedHeight(100)

        self.layout.addLayout(self.file_info_layout)
        self.layout.addWidget(self.list_widget)
        self.layout.addItem(spacer)
        self.layout.addLayout(self.download_location_layout)
        self.layout.addItem(spacer)
        self.layout.addWidget(self.download_button)
        self.layout.addLayout(self.progress_layout)
        self.layout.addWidget(self.log_widget)

        self.setLayout(self.layout)

    def toggle_log_visibility(self, state: int) -> None:
        """Toggle the visibility of the log widget based on the state of the checkbox."""
        if state == 2:
            self.log_widget.setVisible(True)
        elif state == 0:
            self.log_widget.setVisible(False)

    def load_torrent_file(self) -> None:
        """
        Open a dialog for the user to select a torrent file, update the UI.

        Upon selection, update `torrent_path`, `torrent_name`, and call
        `populate_file_list` to refresh the file list in the UI.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Load Torrent File",
            DOWNLOADS_DIR,
            "Torrent Files (*.torrent);;All Files (*)",
            options=options,
        )
        if file_name:
            self.torrent_path = file_name
            self.torrent_name = file_name.split("/")[-1]
            self.setWindowTitle(self.torrent_name)
            self.populate_file_list()

    def populate_file_list(self) -> None:
        """Populate the list widget with available files from the torrent."""
        self.list_widget.clear()
        try:
            result = subprocess.run(
                ["aria2c", "--show-files=true", self.torrent_path],
                capture_output=True,
                text=True,
                check=False,
            )
            result.check_returncode()
            lines = result.stdout.strip().split("\n")
            parsing_files = False  # Flag to indicate when we start parsing file entries
            file_info = ""  # Temporarily store file information across multiple lines
            for line in lines:
                if line.startswith("Files:"): # pylint: disable=R1724
                    parsing_files = True  # Start parsing file entries from now on
                    continue  # Skip the 'Files:' line
                elif parsing_files and line.startswith("---+"):
                    # End of a file entry, add it to the list widget and reset file_info
                    self.list_widget.addItem(file_info.strip())
                    file_info = ""
                elif (
                    parsing_files and line.startswith("idx|") or line.startswith("===+")
                ):
                    # Skip the header line
                    continue
                elif parsing_files and line:
                    file_info += (
                        line + "\n"
                    )  # Accumulate file information across multiple lines
            if file_info:  # Add the last file entry if there is any
                self.list_widget.addItem(file_info.strip())

        except subprocess.CalledProcessError as err:
            print(f"aria2c exited with status {err.returncode}, stderr: {err.stderr}")

    def handle_download(self) -> None:
        """Handle the download based on selection."""
        download_location = self.download_location_textbox.text()
        if self.list_widget.selectedItems():
            selected_items = self.list_widget.selectedItems()
            file_indices = ",".join(
                item.text().split("|")[0] for item in selected_items
            )
        else:
            file_indices = "1-" + str(self.list_widget.count())

        if file_indices:
            self.download_button.setEnabled(False)
            self.progress_bar.setValue(0)
            
            # Start download in a separate thread
            args = [
                "aria2c",
                f"--select-file={file_indices}",
                self.torrent_path,
                f"--dir={download_location}",
                "--summary-interval=2",
                "--allow-overwrite=true",
                "--max-connection-per-server=16",
                "--min-split-size=1M",
                "--file-allocation=none",

            ]
            print(args)
            self.download_thread = DownloadThread(args)
            self.download_thread.progress_update.connect(self.update_progress)
            self.download_thread.log_message.connect(self.append_log_message)
            self.download_thread.download_complete.connect(self.on_download_complete)
            self.download_thread.start()

    def update_progress(self, progress_value: int) -> None:
        """Update the progress bar and label with the current progress value."""
        logging.debug("Progress update: %s", f"{progress_value}%")
        self.progress_bar.setValue(progress_value)
        if progress_value == 100:
            self.download_button.setEnabled(True)

    def on_download_complete(self) -> None:
        """Handle download completion by setting progress to 100%."""
        self.progress_bar.setValue(100)

    def append_log_message(self, message: str) -> None:
        """Append a log message to the log widget."""
        self.log_widget.append(message)


def main() -> None:
    """Main function to run the TorrentDownloader application."""
    app = QApplication(sys.argv)
    downloader = TorrentDownloader()
    downloader.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
