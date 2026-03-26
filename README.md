bobby look look

it's a soundcloud playlist downloader

# soundcloud playlist downloader

download entire soundcloud playlists as a zip file.

## how to use

1. run the exe or `python soundcloud_app.py`
2. paste a soundcloud playlist url
3. click download
4. find your zip in `C:\Users\you\SoundCloudDownloads`

## requirements

- python 3.10+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - `pip install yt-dlp`
- [ffmpeg](https://ffmpeg.org/) - download or `winget install ffmpeg`

## run from source

```bash
git clone https://github.com/stronkbonk/soundcloud-playlist-downloader.git
cd soundcloud-playlist-downloader
pip install yt-dlp
python soundcloud_app.py
```

## build exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name SoundCloudPlaylistDownloader soundcloud_app.py
```
