bobby look look
this is such a cool tool bobby

# soundcloud playlist downloader

download entire soundcloud playlists as a folder.

![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)

## download

EXE:
- **[SoundCloudPlaylistDownloader.exe](https://github.com/howma/soundcloud-zip/releases/latest/download/SoundCloudPlaylistDownloader.exe)**

just double-click and run.

## features

- paste any soundcloud playlist URL
- downloads all available tracks as MP3
- creates a folder automatically
- saves to `C:\Users\YourName\SoundCloudDownloads`

## usage

1. double-click `SoundCloudPlaylistDownloader.exe`
2. paste a soundcloud playlist URL
3. click **FETCH & DOWNLOAD**
4. wait for the folder to be created

## from source

### requirements

- python 3.10+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp): `pip install yt-dlp`
- [ffmpeg](https://ffmpeg.org/): `winget install ffmpeg`

### run

```bash
git clone https://github.com/howma/soundcloud-zip.git
cd soundcloud-zip
pip install yt-dlp
python soundcloud_app.py
```

## build exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name SoundCloudPlaylistDownloader soundcloud_app.py
```

the exe will be in the `dist` folder.


