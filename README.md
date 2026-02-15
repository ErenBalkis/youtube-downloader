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
| �️ **One-Click Desktop Launch** | Batch scripts for instant setup and launch — no terminal knowledge needed |

---

## 🚀 Quick Start (One-Click Setup)

### Prerequisites

- **Python 3.10+** — [Download](https://python.org) (check "Add Python to PATH" during install)
- **ffmpeg** — [Download](https://ffmpeg.org/download.html) and extract to `C:\ffmpeg\` (auto-detected)

### Step 1 — Install

Double-click **`install_env.bat`**. It will:
- ✅ Check Python is installed
- ✅ Create a virtual environment (`venv/`)
- ✅ Install all dependencies automatically

### Step 2 — Launch

Double-click **`run_app.bat`**. The app opens in your default browser at **http://localhost:8501**.

> [!TIP]
> Create a Desktop Shortcut for `run_app.bat` so you can launch the app like any other program — see [Desktop Shortcut](#-desktop-shortcut) below.

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

## 🖥️ Desktop Shortcut

Turn `run_app.bat` into a professional-looking desktop app:

### Create the Shortcut

1. Open the project folder in File Explorer
2. **Right-click** `run_app.bat` → **Send to** → **Desktop (create shortcut)**
3. A shortcut named *"run_app.bat - Shortcut"* appears on your Desktop

### Rename & Set Icon

4. **Right-click** the shortcut on your Desktop → **Properties**
5. In the **General** tab, rename it to **YouTube Downloader**
6. Click **Change Icon…** → **Browse…**
7. Navigate to the project's `assets\app_icon.ico` and select it
8. Click **OK** → **Apply** → **OK**

> [!NOTE]
> A custom `.ico` file is included at `assets/app_icon.ico`. You can replace it with any `.ico` file you prefer.

### Optional: Minimize Console Window

To hide the black console window when launching:

4. **Right-click** the shortcut → **Properties**
5. Set **Run** to **Minimized**
6. Click **Apply** → **OK**

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
├── install_env.bat     # One-click environment setup
├── run_app.bat         # One-click app launcher
├── requirements.txt    # Python dependencies
├── generate_icon.py    # Icon generator utility
├── assets/
│   └── app_icon.ico    # Desktop shortcut icon
├── .gitignore          # Git ignore rules
├── LICENSE             # MIT License
└── README.md           # This file
```

---

## ⚙️ ffmpeg Auto-Detection

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

---

<div align="center">
Built with ❤️ using Streamlit & yt-dlp
</div>
