import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from torrento import TorrentDownloader

@pytest.fixture(scope='session')
def qapp():
    return QApplication([])

def test_window_title(qapp):
    torrent_path = "example.torrent"
    torrent_name = "Example"
    downloader = TorrentDownloader(torrent_path, torrent_name)
    assert downloader.windowTitle() == "Example"

def test_download_location_default_value(qapp):
    torrent_path = "example.torrent"
    torrent_name = "Example"
    downloader = TorrentDownloader(torrent_path, torrent_name)
    assert downloader.download_location_textbox.text() == "/Users/sivanagendra/Downloads/"

def test_list_widget_populated(qapp, mocker):
    torrent_path = "example.torrent"
    torrent_name = "Example"
    downloader = TorrentDownloader(torrent_path, torrent_name)
    mocker.patch.object(downloader, 'populate_file_list', return_value=None)
    downloader.populate_file_list()
    assert downloader.list_widget.count() > 0

def test_progress_bar_initial_value(qapp):
    torrent_path = "example.torrent"
    torrent_name = "Example"
    downloader = TorrentDownloader(torrent_path, torrent_name)
    assert downloader.progress_bar.value() == 0

def test_click_download_selected_button(qapp, qtbot, mocker):
    torrent_path = "example.torrent"
    torrent_name = "Example"
    downloader = TorrentDownloader(torrent_path, torrent_name)
    mocker.patch.object(downloader, 'download_selected_files', return_value=None)
    qtbot.mouseClick(downloader.download_button, Qt.LeftButton)
    downloader.download_selected_files.assert_called_once()
