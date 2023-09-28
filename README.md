# Torronto - Torrent Downloader 🚀

Torronto is a streamlined and intuitive torrent downloader built with Python and Qt. It provides a friendly graphical user interface to manage torrent downloads efficiently. Whether you're downloading a single file or a bunch, Torronto has got you covered.


## Features 🌟

- Graphical User Interface for selecting and downloading torrent files
- Supports individual file selection within a torrent
- Real-time progress monitoring
- Ability to specify download directory
- Multi-threaded downloads for optimized speed

## Getting Started 🛠

These instructions will help you set up and run Torronto on your machine.

### Prerequisites

- Python 3.x installed on your machine.
- PySide6 installed in your Python environment.
- aria2c installed on your machine.

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Torronto.git
cd Torronto
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

### Usage

1. To start the application, run the following command in the terminal:
```bash
python torronto.py <torrent path>
```
Replace `<torrent path>` with the path to your torrent file.

2. The UI will display the list of available files in the torrent. Select the files you wish to download.
3. Specify the download location in the provided text box.
4. Click on "Download Selected" to download the selected files or "Download All" to download all files.
5. Monitor the progress through the progress bar and percentage label displayed.

## Contributing 🤝

Feel free to submit issues, or open pull requests to improve Torronto. All contributions are welcome!

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- PySide6 for the robust Qt bindings.
- aria2 for the efficient download utility.