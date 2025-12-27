YouTube Downloader (Max 1080p)

This is a simple desktop YouTube downloader built with Python, CustomTkinter, and pytubefix.
The application downloads YouTube videos at a maximum resolution of 1080p with audio by automatically
selecting the best available streams and merging video and audio using FFmpeg.

The project is intentionally limited to 1080p to ensure reliable audio playback, MP4 compatibility,
and stable downloads across different systems.

FEATURES
- Desktop GUI built with CustomTkinter
- Downloads videos up to 1080p maximum
- Audio is always included
- Automatic best stream selection
- MP4 output format
- Safe file naming
- Simple and lightweight

REQUIREMENTS
- Python 3.9 or newer
- FFmpeg installed and available in system PATH

INSTALLATION
1. Clone the repository
2. Install dependencies using pip:
   pip install pytubefix customtkinter

FFMPEG SETUP
FFmpeg is required to merge video and audio streams.
Download a static build from https://ffmpeg.org/download.html
Add the bin directory to system PATH.
Verify installation using:
ffmpeg -version

USAGE
Run the application using:
python main.py

Paste a YouTube link and click "Download Max 1080p".
The downloaded video will be saved in the downloads folder.

OUTPUT DETAILS
- Output format: MP4
- Maximum resolution: 1080p
- Audio included
- Higher resolutions are intentionally disabled

LIMITATIONS
Some videos may not provide a 1080p stream.
Private or restricted videos may fail.
FFmpeg must be accessible via PATH.

WHY 1080P ONLY
Higher resolutions use adaptive streams and may cause compatibility issues.
Limiting to 1080p ensures stability and audio reliability.

LICENSE AND DISCLAIMER
This project is for educational and personal use only.
Downloading copyrighted content may violate YouTube’s Terms of Service.
This project is not affiliated with YouTube.

