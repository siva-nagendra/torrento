import pytest
from PySide6.QtWidgets import QApplication
from torrento import TorrentDownloader


@pytest.fixture(scope="session")
def app():
    return QApplication([])


@pytest.fixture
def downloader(app):
    return TorrentDownloader()
