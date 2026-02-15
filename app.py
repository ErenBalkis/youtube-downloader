"""
YouTube Downloader — Streamlit + yt-dlp
========================================
A polished, single-page Streamlit application that lets users paste a YouTube
URL, preview the video (thumbnail + title), choose a format (MP3 audio or
MP4 video with resolution picker), and download the result.

Requirements:
    pip install streamlit yt-dlp
    System: ffmpeg must be on $PATH for stream merging / MP3 conversion.

Run:
    streamlit run app.py
"""

import os
import re
import shutil
import tempfile
from pathlib import Path

import streamlit as st
import yt_dlp

# ─────────────────────────────────────────────
# Page configuration & custom CSS
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="YouTube Downloader",
    page_icon="🎬",
    layout="centered",
)

CUSTOM_CSS = """
<style>
    /* ── Global ─────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Header ─────────────────────────────── */
    .main-header {
        text-align: center;
        padding: 1.5rem 0 0.5rem;
    }
    .main-header h1 {
        background: linear-gradient(135deg, #FF0000 0%, #FF4E50 50%, #F9D423 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.4rem;
        margin-bottom: 0.2rem;
    }
    .main-header p {
        color: #888;
        font-size: 1rem;
    }

    /* ── Card container ─────────────────────── */
    .video-card {
        background: linear-gradient(145deg, #1e1e2f, #2a2a3d);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    }
    .video-card img {
        border-radius: 12px;
        width: 100%;
    }
    .video-card h3 {
        color: #f1f1f1;
        margin-top: 0.8rem;
        font-size: 1.15rem;
        font-weight: 600;
    }
    .video-card .meta {
        color: #aaa;
        font-size: 0.85rem;
        margin-top: 0.25rem;
    }

    /* ── Footer ─────────────────────────────── */
    .footer {
        text-align: center;
        color: #555;
        font-size: 0.78rem;
        margin-top: 2rem;
        padding-bottom: 1rem;
    }

    /* ── Misc polish ────────────────────────── */
    div.stDownloadButton > button {
        background: linear-gradient(135deg, #FF4E50, #F9D423);
        color: #fff;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    div.stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 78, 80, 0.4);
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Helper: locate ffmpeg on the system
# ─────────────────────────────────────────────
_FFMPEG_SEARCH_DIRS = [
    r"C:\ffmpeg\bin",
    r"C:\Program Files\ffmpeg\bin",
    r"C:\Program Files (x86)\ffmpeg\bin",
    os.path.expanduser(r"~\ffmpeg\bin"),
    os.path.expanduser(r"~\Downloads\ffmpeg\bin"),
]


def _find_ffmpeg() -> str | None:
    """
    Locate the directory containing ffmpeg.exe.
    Checks the system PATH first, then common Windows install locations.
    Returns the directory path or None if not found.
    """
    # 1. Check PATH
    path_result = shutil.which("ffmpeg")
    if path_result:
        return str(Path(path_result).parent)

    # 2. Check common Windows locations
    for search_dir in _FFMPEG_SEARCH_DIRS:
        candidate = os.path.join(search_dir, "ffmpeg.exe")
        if os.path.isfile(candidate):
            return search_dir

    # 3. Recursive search in C:\ffmpeg (covers nested extractions)
    ffmpeg_root = r"C:\ffmpeg"
    if os.path.isdir(ffmpeg_root):
        for root, _dirs, files in os.walk(ffmpeg_root):
            if "ffmpeg.exe" in files:
                return root

    return None


# Cache the result so we only search once per app run
FFMPEG_DIR: str | None = _find_ffmpeg()


def _ffmpeg_available() -> bool:
    """Return True if ffmpeg was found anywhere on the system."""
    return FFMPEG_DIR is not None


# ─────────────────────────────────────────────
# Helper: validate YouTube URL
# ─────────────────────────────────────────────
_YT_REGEX = re.compile(
    r"^(https?://)?(www\.)?"
    r"(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)"
    r"[\w\-]{11}"
)


def is_valid_youtube_url(url: str) -> bool:
    """Quick regex check before hitting the network."""
    return bool(_YT_REGEX.search(url.strip()))


# ─────────────────────────────────────────────
# Core: fetch video metadata
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False, ttl=600)
def get_video_info(url: str) -> dict | None:
    """
    Extract video metadata (title, thumbnail, available formats)
    without downloading any content.

    Returns a dict with keys: title, thumbnail, formats, duration, uploader
    or None on failure.
    """
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        # 'extract_flat' is intentionally NOT set so we get full format list
    }
    if FFMPEG_DIR:
        ydl_opts["ffmpeg_location"] = FFMPEG_DIR
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title", "Unknown Title"),
                "thumbnail": info.get("thumbnail", ""),
                "formats": info.get("formats", []),
                "duration": info.get("duration", 0),
                "uploader": info.get("uploader", "Unknown"),
                "view_count": info.get("view_count", 0),
            }
    except yt_dlp.utils.DownloadError as exc:
        st.error(f"❌ Could not fetch video info: {exc}")
        return None
    except Exception as exc:  # noqa: BLE001
        st.error(f"❌ An unexpected error occurred: {exc}")
        return None


# ─────────────────────────────────────────────
# Core: parse available resolutions
# ─────────────────────────────────────────────
def get_available_resolutions(formats: list[dict]) -> list[str]:
    """
    Deduplicate and sort video resolutions available for download.
    Returns labels like ['1080p', '720p', '480p', '360p', '240p', '144p'].
    """
    heights: set[int] = set()
    for fmt in formats:
        # Only consider formats that have a video stream
        if fmt.get("vcodec", "none") != "none" and fmt.get("height"):
            heights.add(fmt["height"])

    # Sort descending and format as labels
    return [f"{h}p" for h in sorted(heights, reverse=True)]


# ─────────────────────────────────────────────
# Core: download content
# ─────────────────────────────────────────────
def download_content(
    url: str,
    fmt: str,
    resolution: str | None,
    tmp_dir: str,
    progress_bar,
    status_text,
) -> str | None:
    """
    Download the video/audio into *tmp_dir* and return the path to the
    resulting file, or None on failure.

    Parameters
    ----------
    url : str
        YouTube video URL.
    fmt : str
        "audio" or "video".
    resolution : str | None
        e.g. "720p" — only required when *fmt* is "video".
    tmp_dir : str
        Temporary directory to store downloaded files.
    progress_bar : streamlit progress bar widget
    status_text : streamlit empty widget for status messages
    """

    def _progress_hook(d: dict) -> None:
        """yt-dlp progress callback → update Streamlit widgets."""
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            downloaded = d.get("downloaded_bytes", 0)
            if total > 0:
                pct = min(downloaded / total, 1.0)
                progress_bar.progress(pct, text=f"Downloading… {pct:.0%}")
            else:
                status_text.text("Downloading… (size unknown)")
        elif d["status"] == "finished":
            progress_bar.progress(1.0, text="Download complete — processing…")

    output_template = os.path.join(tmp_dir, "%(title)s.%(ext)s")

    if fmt == "audio":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_template,
            "quiet": True,
            "no_warnings": True,
            "progress_hooks": [_progress_hook],
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }
        if FFMPEG_DIR:
            ydl_opts["ffmpeg_location"] = FFMPEG_DIR
    else:
        # Extract numeric height from label like "720p"
        height = resolution.replace("p", "") if resolution else "720"
        ydl_opts = {
            "format": (
                f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"
            ),
            "outtmpl": output_template,
            "quiet": True,
            "no_warnings": True,
            "merge_output_format": "mp4",
            "progress_hooks": [_progress_hook],
        }
        if FFMPEG_DIR:
            ydl_opts["ffmpeg_location"] = FFMPEG_DIR

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Find the resulting file in the temp directory
        files = list(Path(tmp_dir).iterdir())
        if files:
            return str(files[0])
        st.error("❌ Download succeeded but no output file was found.")
        return None
    except yt_dlp.utils.DownloadError as exc:
        st.error(f"❌ Download failed: {exc}")
        return None
    except Exception as exc:  # noqa: BLE001
        st.error(f"❌ Unexpected error during download: {exc}")
        return None


# ─────────────────────────────────────────────
# Helper: format duration
# ─────────────────────────────────────────────
def _fmt_duration(seconds: int) -> str:
    """Convert seconds to a human-readable duration string."""
    if seconds <= 0:
        return "Unknown"
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}h {m}m {s}s"
    return f"{m}m {s}s"


def _fmt_views(n: int) -> str:
    """Abbreviate large view counts."""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M views"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K views"
    return f"{n} views"


# ─────────────────────────────────────────────
# Helper: clean up old temp directory
# ─────────────────────────────────────────────
def _cleanup_temp() -> None:
    """Remove previously created temp directory from session state."""
    old_dir = st.session_state.get("tmp_dir")
    if old_dir and os.path.isdir(old_dir):
        shutil.rmtree(old_dir, ignore_errors=True)
    st.session_state["tmp_dir"] = None
    st.session_state["downloaded_file"] = None
    st.session_state["download_ready"] = False


# ═════════════════════════════════════════════
# UI
# ═════════════════════════════════════════════

# ── Header ──────────────────────────────────
st.markdown(
    '<div class="main-header">'
    "<h1>🎬 YouTube Downloader</h1>"
    "<p>Paste a YouTube link, pick a format, and download instantly.</p>"
    "</div>",
    unsafe_allow_html=True,
)

# ── ffmpeg warning ──────────────────────────
if not _ffmpeg_available():
    st.warning(
        "⚠️ **ffmpeg** was not found on your system PATH. "
        "MP3 conversion and high-quality MP4 merging require ffmpeg. "
        "[Download ffmpeg →](https://ffmpeg.org/download.html)"
    )

# ── Initialise session state ────────────────
for key, default in {
    "video_info": None,
    "downloaded_file": None,
    "download_ready": False,
    "tmp_dir": None,
    "last_url": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── URL input ───────────────────────────────
url = st.text_input(
    "🔗 YouTube URL",
    placeholder="https://www.youtube.com/watch?v=...",
    help="Paste a full YouTube video or Shorts URL.",
)

# Reset state when URL changes
if url != st.session_state["last_url"]:
    _cleanup_temp()
    st.session_state["video_info"] = None
    st.session_state["last_url"] = url

# ── Fetch & display video info ──────────────
if url:
    if not is_valid_youtube_url(url):
        st.error("🚫 That doesn't look like a valid YouTube URL. Please check and try again.")
    else:
        with st.spinner("Fetching video information…"):
            info = get_video_info(url)

        if info:
            st.session_state["video_info"] = info

            # ── Video preview card ──────────
            st.markdown(
                '<div class="video-card">'
                f'<img src="{info["thumbnail"]}" alt="thumbnail" />'
                f'<h3>{info["title"]}</h3>'
                f'<p class="meta">'
                f'{info["uploader"]}  •  '
                f'{_fmt_duration(info["duration"])}  •  '
                f'{_fmt_views(info["view_count"])}'
                f"</p>"
                "</div>",
                unsafe_allow_html=True,
            )

            # ── Format selection ────────────
            st.divider()
            format_choice = st.radio(
                "📦 Choose format",
                ["🎵 Audio Only (MP3)", "🎥 Video (MP4)"],
                horizontal=True,
            )

            selected_resolution = None
            if "Video" in format_choice:
                resolutions = get_available_resolutions(info["formats"])
                if resolutions:
                    selected_resolution = st.selectbox(
                        "📐 Select resolution", resolutions
                    )
                else:
                    st.warning("No video-only streams found. The best available format will be used.")
                    selected_resolution = None

            # ── Download trigger ────────────
            st.divider()
            if st.button("⬇️  Start Download", use_container_width=True, type="primary"):
                _cleanup_temp()

                # Create a fresh temp directory
                tmp_dir = tempfile.mkdtemp(prefix="ytdl_")
                st.session_state["tmp_dir"] = tmp_dir

                progress_bar = st.progress(0, text="Preparing…")
                status_text = st.empty()

                fmt = "audio" if "Audio" in format_choice else "video"
                file_path = download_content(
                    url, fmt, selected_resolution, tmp_dir, progress_bar, status_text
                )

                if file_path and os.path.isfile(file_path):
                    st.session_state["downloaded_file"] = file_path
                    st.session_state["download_ready"] = True
                    progress_bar.progress(1.0, text="✅ Ready!")
                    status_text.empty()
                else:
                    progress_bar.empty()

            # ── Offer file to user ──────────
            if st.session_state.get("download_ready") and st.session_state.get("downloaded_file"):
                file_path = st.session_state["downloaded_file"]
                file_name = os.path.basename(file_path)
                mime = "audio/mpeg" if file_name.endswith(".mp3") else "video/mp4"

                with open(file_path, "rb") as fh:
                    st.download_button(
                        label=f"💾  Save **{file_name}**",
                        data=fh,
                        file_name=file_name,
                        mime=mime,
                        use_container_width=True,
                    )

# ── Footer ──────────────────────────────────
st.markdown(
    '<div class="footer">'
    "Built with ❤️ using Streamlit & yt-dlp  •  "
    "ffmpeg required for best results"
    "</div>",
    unsafe_allow_html=True,
)
