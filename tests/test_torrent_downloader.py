import pytest
from unittest.mock import MagicMock
from torrento import (
    TorrentDownloader,
)  # Assuming your file is named torrent_downloader.py


def test_toggle_log_visibility(app, downloader):
    downloader.more_info_checkbox.setChecked(True)
    assert downloader.log_widget.isVisible() is True
    downloader.more_info_checkbox.setChecked(False)
    assert downloader.log_widget.isVisible() is False


def test_load_torrent_file(app, downloader, mocker):
    mock_get_open_file_name = mocker.patch(
        "PySide6.QtWidgets.QFileDialog.getOpenFileName",
        return_value=("example.torrent", "Torrent Files (*.torrent);;All Files (*)"),
    )
    downloader.load_torrent_file()
    mock_get_open_file_name.assert_called_once()
    assert downloader.torrent_path == "example.torrent"
    assert downloader.torrent_name == "example.torrent"


def test_populate_file_list(app, downloader, mocker):
    downloader.torrent_path = "example.torrent"
    mock_subprocess_run = mocker.patch(
        "subprocess.run",
        return_value=MagicMock(
            stdout="Files:\nsome output\n---+\n1| file1.txt | 10MB\n2| file2.txt | 20MB\n"
        ),
    )
    downloader.populate_file_list()
    mock_subprocess_run.assert_called_once()
    assert downloader.list_widget.count() == 2


def test_handle_download(app, downloader, mocker):
    mock_download_thread = mocker.patch(
        "torrent_downloader.DownloadThread", autospec=True
    )
    downloader.torrent_path = "example.torrent"
    downloader.handle_download()
    mock_download_thread.assert_called_once_with(
        [
            "aria2c",
            "--select-file=1-0",
            "example.torrent",
            "--dir=/Users/username/Downloads",
            "--summary-interval=0.1",
            "--allow-overwrite=true",
            "--max-connection-per-server=16",
            "--min-split-size=1M",
        ]
    )


def test_update_progress(app, downloader):
    downloader.update_progress(50)
    assert downloader.progress_bar.value() == 50
    downloader.update_progress(100)
    assert downloader.progress_bar.value() == 100
    assert downloader.download_button.isEnabled() is True


def test_on_download_complete(app, downloader):
    downloader.on_download_complete()
    assert downloader.progress_bar.value() == 100


def test_append_log_message(app, downloader):
    downloader.append_log_message("Test log message")
    assert downloader.log_widget.toPlainText() == "Test log message\n"
