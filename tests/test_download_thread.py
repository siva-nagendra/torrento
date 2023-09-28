import pytest
from unittest.mock import MagicMock
from torrento import DownloadThread


def test_run(app, qtbot, mocker):
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

    thread = DownloadThread(["aria2c", "some arguments"])
    qtbot.connect_signal(thread.progress_update, lambda value: None)
    qtbot.connect_signal(thread.log_message, lambda message: None)
    qtbot.connect_signal(thread.download_complete, lambda: None)

    with qtbot.waitSignal(thread.download_complete, timeout=5000):
        thread.start()

    assert mock_popen.call_count == 1  # Check that Popen was called exactly once
    assert (
        thread.progress_update.emit.call_count == 2
    )  # Check the number of progress updates
    assert thread.log_message.emit.call_count == 4  # Check the number of log messages
    assert (
        thread.download_complete.emit.call_count == 1
    )  # Check that download_complete was emitted


def test_stop(app):
    thread = DownloadThread(["aria2c", "some arguments"])
    mock_process = MagicMock()
    thread.process = mock_process
    thread.stop()
    mock_process.terminate.assert_called_once()  # Check that process.terminate() was called
