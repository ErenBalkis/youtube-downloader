<div align="center">

# 🎬 YouTube Downloader

**A sleek, modern YouTube downloader built with Streamlit and yt-dlp.**

Download YouTube videos in MP4 or extract audio as MP3 — all from your browser.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.54+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Video Preview** | Fetches and displays the video thumbnail, title, uploader, duration and view count |
| 🎵 **Audio Download** | Download best-quality audio and convert to MP3 |
| 🎥 **Video Download** | Download video in your chosen resolution (1080p, 720p, 480p, etc.) |
| 📊 **Progress Bar** | Real-time download progress tracking |
| 🛡️ **Error Handling** | Friendly messages for invalid URLs, restricted videos, and missing dependencies |
| 🔎 **Auto ffmpeg Detection** | Automatically finds ffmpeg on common Windows install paths — no PATH setup needed |

---

## 📸 Screenshot

<div align="center">
<img src="assets/screenshot.png" alt="YouTube Downloader Screenshot" width="700"/>
</div>

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **ffmpeg** — required for MP3 conversion and merging video+audio streams
  - [Download ffmpeg](https://ffmpeg.org/download.html) and either add it to your PATH or place it in `C:\ffmpeg\bin\`

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/youtube-downloader.git
cd youtube-downloader

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open in your browser at **http://localhost:8501**.

---

## 📖 Usage

1. **Paste** a YouTube URL into the input field
2. **Preview** the video details (thumbnail, title, channel, duration)
3. **Choose** your format:
   - 🎵 **Audio Only (MP3)** — extracts best audio and converts to MP3
   - 🎥 **Video (MP4)** — select your preferred resolution from the dropdown
4. **Click** "Start Download" and watch the progress bar
5. **Save** the file using the download button that appears

---

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io/)** — Web UI framework
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** — YouTube video/audio extraction
- **[ffmpeg](https://ffmpeg.org/)** — Media processing (stream merging & MP3 conversion)

---

## 📁 Project Structure

```
youtube-downloader/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
├── LICENSE             # MIT License
└── README.md           # This file
```

---

## ⚙️ Configuration

The app automatically detects ffmpeg in these locations (Windows):

| Priority | Location |
|---|---|
| 1 | System PATH |
| 2 | `C:\ffmpeg\bin\` |
| 3 | `C:\Program Files\ffmpeg\bin\` |
| 4 | `~\ffmpeg\bin\` |
| 5 | `~\Downloads\ffmpeg\bin\` |

If ffmpeg is not found, the app displays a warning with a download link.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
