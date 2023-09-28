name = "torrento"

version = "0.1.0"

authors = ["Siva Nagendra"]

description = "Torrent Downloader using PySide6 and aria2c."

requires = [
    "python-3.10",
    "PySide6",
]

build_command = "python {root}/setup.py install"

test_requires = ["black", "pylint", "pytest", "pytest-qt"]

tests = {
    "black": "black --check .",
    "pylint": "pylint torrento.py",
    "pytest": "pytest tests/test_torrento.py -v",
    "pytest_quiet": "pytest tests/test_torrento.py -q",  # Quiet mode
}


def commands():
    env.PATH.append("{root}/bin")
    env.PYTHONPATH.append("{root}/python")
