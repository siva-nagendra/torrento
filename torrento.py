import sys
import subprocess
import re
from typing import List
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QProgressBar,
    QLabel,
    QLineEdit,
)
from PySide6.QtCore import QThread, Signal

class DownloadThread(QThread):
    """Thread to handle the download process."""
    progress_update: Signal = Signal(int)

    def __init__(self, args: List[str]) -> None:
        """Initialize the DownloadThread with the necessary arguments for aria2c."""
        super().__init__()
        self.args = args

    def run(self) -> None:
        """Run the download process and emit progress updates."""
        try:
            process = subprocess.Popen(
                self.args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                universal_newlines=True,
            )
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                progress = re.search(r"\((\d+)%\)", line)
                if progress:
                    progress_value = int(progress.group(1))
                    self.progress_update.emit(progress_value)
            process.wait()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


class TorrentDownloader(QWidget):
    """Widget to handle the torrent downloading UI and functionality."""
    def __init__(self, torrent_path: str, torrent_name: str) -> None:
        """Initialize the TorrentDownloader with the path and name of the torrent."""
        super().__init__()
        self.torrent_path = torrent_path
        self.torrent_name = torrent_name
        self.download_thread = None
        self.init_ui()

    def init_ui(self) -> None:
        """Initialize the UI components."""
        self.setWindowTitle(self.torrent_name)
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # Add a label to indicate available files
        available_label = QLabel("Available Files:")
        

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        self.populate_file_list()

        self.download_button = QPushButton("Download Selected")
        self.download_button.clicked.connect(self.download_selected_files)

        # Add a "Download All" button
        self.download_all_button = QPushButton("Download All")
        self.download_all_button.clicked.connect(self.download_all_files)

        # Create a horizontal layout for the progress components
        self.progress_layout = QHBoxLayout()

        # Create and add the Progress label, ProgressBar, and Progress Percentage label to the horizontal layout
        self.progress_label = QLabel("Progress:")
        self.progress_bar = QProgressBar()
        self.progress_percentage_label = QLabel("0%")

        self.progress_layout.addWidget(self.progress_label)
        self.progress_layout.addWidget(self.progress_bar)
        self.progress_layout.addWidget(self.progress_percentage_label)

        # Add a download location textbox with default value
        self.download_location_label = QLabel("Download Location:")
        self.download_location_textbox = QLineEdit("/Users/sivanagendra/Downloads/")
        
        self.layout.addWidget(self.download_location_label)
        self.layout.addWidget(self.download_location_textbox)
        self.layout.addWidget(available_label)
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.download_button)
        self.layout.addWidget(self.download_all_button)
        self.layout.addLayout(self.progress_layout)

        self.setLayout(self.layout)

    def populate_file_list(self) -> None:
        """Populate the list widget with available files from the torrent."""
        try:
            result = subprocess.run(
                ["aria2c", "--show-files=true", self.torrent_path],
                capture_output=True,
                text=True,
            )
            result.check_returncode()  # This will raise an exception if aria2c exits with a non-zero status
            lines = result.stdout.strip().split("\n")
            parsing_files = False  # Flag to indicate when we start parsing file entries
            file_info = ""  # Temporarily store file information across multiple lines
            for line in lines:
                if line.startswith("Files:"):
                    parsing_files = True  # Start parsing file entries from now on
                    continue  # Skip the 'Files:' line
                elif parsing_files and line.startswith("---+"):
                    # End of a file entry, add it to the list widget and reset file_info
                    self.list_widget.addItem(file_info.strip())
                    file_info = ""
                elif parsing_files and line:
                    file_info += (
                        line + "\n"
                    )  # Accumulate file information across multiple lines
            if file_info:  # Add the last file entry if there is any
                return self.list_widget.addItem(file_info.strip())
        except subprocess.CalledProcessError as e:
            print(f"aria2c exited with status {e.returncode}, stderr: {e.stderr}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def download_selected_files(self) -> None:
        """Download the selected files."""
        selected_items = self.list_widget.selectedItems()
        file_indices = ",".join(item.text().split("|")[0] for item in selected_items)
        download_location = self.download_location_textbox.text()
        if file_indices:
            self.download_button.setEnabled(False)
            self.progress_bar.setValue(0)
            self.progress_label.setText("Progress: 0%")

            # Start download in a separate thread
            args = [
                "aria2c",
                f"--select-file={file_indices}",
                self.torrent_path,
                f"--dir={download_location}",
                "--max-connection-per-server=16",
                "--min-split-size=1M",
                "--summary-interval=1",
                "--allow-overwrite=true",
            ]
            print(args)
            self.download_thread = DownloadThread(args)
            self.download_thread.progress_update.connect(self.update_progress)
            self.download_thread.start()
            if not self.download_thread.gid:
                print("Failed to get gid")
                return

    def download_all_files(self) -> None:
        """Download all files if none are selected, otherwise download the selected files."""
        if not self.list_widget.selectedItems():
            # If no items are selected, download all files
            file_indices = "1-" + str(self.list_widget.count())
        else:
            # If some items are selected, download the selected files
            selected_items = self.list_widget.selectedItems()
            file_indices = ",".join(
                item.text().split("|")[0] for item in selected_items
            )

        download_location = self.download_location_textbox.text()
        if file_indices:
            self.download_button.setEnabled(False)
            self.download_all_button.setEnabled(
                False
            )  # Disable the "Download All" button
            self.progress_bar.setValue(0)
            self.progress_label.setText("Progress: 0%")

            # Start download in a separate thread
            args = [
                "aria2c",
                f"--select-file={file_indices}",
                self.torrent_path,
                f"--dir={download_location}",
                "--max-connection-per-server=16",
                "--min-split-size=1M",
                "--summary-interval=1",
            ]
            self.download_thread = DownloadThread(args)
            self.download_thread.progress_update.connect(self.update_progress)
            self.download_thread.start()

    def update_progress(self, progress_value: int) -> None:
        """Update the progress bar and label with the current progress value."""
        self.progress_bar.setValue(progress_value)
        self.progress_percentage_label.setText(f"{progress_value}%")
        if progress_value == 100:
            self.download_button.setEnabled(True)
            self.download_all_button.setEnabled(True)
            self.progress_percentage_label.setText("Download complete")


def main(torrent_path: str) -> None:
    """Main function to run the TorrentDownloader application."""
    app = QApplication(sys.argv)
    torrent_name = torrent_path.split("/")[-1]
    downloader = TorrentDownloader(torrent_path, torrent_name)
    downloader.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: torrento.py <torrent path>")
        sys.exit(1)
    main(sys.argv[1])