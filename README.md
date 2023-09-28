# Torrento - Torrent Downloader 🚀

Torrento is a streamlined and intuitive torrent downloader built with Python, Qt (PySide6), and aria2c. It provides a clean and simple graphical user interface for those who are tired of the ad-ridden traditional free torrent clients. Manage your torrent downloads efficiently with Torrento.

## Features 🌟

- Graphical User Interface for selecting and downloading torrent files.
- Supports individual file selection within a torrent.
- Real-time progress monitoring.
- Ability to specify download directory.
- Multi-threaded downloads for optimized speed.
- Enhanced log visibility control to toggle between verbose and quiet logging.
- Integrated with Rez for environment management.
- Automated tests for ensuring code quality, formatting, and functionality.
- Black for code formatting and Pylint for code quality checks.

## Getting Started 🛠

These instructions will help you set up and run Torrento on your machine.

### Prerequisites

- Python 3.x installed on your machine.
- PySide6 installed in your Python environment.
- aria2c installed on your machine.
- Rez (for environment management).

### Installation

1. Clone the repository:
```bash
git clone https://github.com/siva-nagendra/torrento
cd Torrento
```

2. (Optional) Set up Rez environment:
```bash
# Ensure Rez is installed on your machine
pip install rez

# Create a directory for Rez packages if it doesn't exist
mkdir ~/packages

# Set the REZ_PACKAGES_PATH environment variable
export REZ_PACKAGES_PATH=~/packages
```

### Usage

1. To start the application with Rez, run the following command in the terminal:
```bash
rez-env torrento -- python Torrento.py
```
   Or without Rez:
```bash
python Torrento.py
```

2. Load a torrent file by clicking on "Load Torrent" button and select the torrent file you wish to download.
3. The UI will display the list of available files in the torrent. Select the files you wish to download.
4. Specify the download location in the provided text box.
5. Click on "Download" to start downloading.
6. Monitor the progress through the progress bar, and toggle verbose logging by checking/unchecking the "More info" checkbox.

## Testing and Quality Assurance 🧪

- To run tests, execute the following command in the terminal:
```bash
./run_tests.sh
```
For quiet mode testing:
```bash
./run_tests.sh quiet
```

- To check code formatting and quality, use the Rez environment and run:
```bash
rez-build --install --test
```

## Contributing 🤝

Feel free to submit issues, or open pull requests to improve Torrento. All contributions are welcome!

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.