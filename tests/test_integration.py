import pytest
from unittest.mock import MagicMock
from torrento import TorrentDownloader, DownloadThread


def test_download_process_integration(app, downloader, mocker):
    mock_subprocess_run = mocker.patch(
        "subprocess.run",
        return_value=MagicMock(
            stdout="Files:\nsome output\n---+\n1| file1.txt | 10MB\n2| file2.txt | 20MB\n"
        ),
    )
    downloader.torrent_path = "example.torrent"
    downloader.populate_file_list()

    mock_popen = mocker.patch("subprocess.Popen", autospec=True)
    mock_process = MagicMock()
    mock_popen.return_value = mock_process
    mock_process.stdout.readline.side_effect = [
        "some irrelevant output",
        "(10%) - Download progress update",
        "(50%) - Download progress update",
        "Download of selected files was complete",
        "",
    ]

    downloader.handle_download()
    assert downloader.progress_bar.value() == 100


# You may add more integration tests to cover other scenarios and interactions between classes
