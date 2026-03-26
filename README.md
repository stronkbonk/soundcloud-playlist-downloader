# SoundCloud Playlist Downloader

Download entire SoundCloud playlists as a ZIP file.

![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Download

Get the ready-to-use executable:
- **[SoundCloudPlaylistDownloader.exe](https://github.com/howma/soundcloud-zip/releases/latest/download/SoundCloudPlaylistDownloader.exe)**

No installation required. Just double-click and run.

## Features

- Paste any SoundCloud playlist URL
- Downloads all available tracks as MP3
- Creates a ZIP file automatically
- Saves to `C:\Users\YourName\SoundCloudDownloads`

## Usage

1. Double-click `SoundCloudPlaylistDownloader.exe`
2. Paste a SoundCloud playlist URL
3. Click **FETCH & DOWNLOAD**
4. Wait for the ZIP file to be created

## From Source

### Requirements

- Python 3.10+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp): `pip install yt-dlp`
- [ffmpeg](https://ffmpeg.org/): `winget install ffmpeg`

### Run

```bash
git clone https://github.com/howma/soundcloud-zip.git
cd soundcloud-zip
pip install yt-dlp
python soundcloud_app.py
```

## Build EXE

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name SoundCloudPlaylistDownloader soundcloud_app.py
```

The EXE will be in the `dist` folder.

## Requirements

- **yt-dlp** - Downloads audio from SoundCloud
- **ffmpeg** - Converts audio to MP3

Without these, the app won't work. Install them before running.
