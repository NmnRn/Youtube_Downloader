import os
import re
import threading
import subprocess
from datetime import timedelta
import customtkinter as ctk
from tkinter import messagebox
from pytubefix import YouTube

FFMPEG_PATH = "PATH"

ctk.set_appearance_mode("dark")

window = ctk.CTk()
window.minsize(440, 560)
window.title("YouTube Downloader")

header = ctk.CTkLabel(window, text="YouTube Downloader", font=("Arial", 22))
header.pack(pady=(20, 10))

label = ctk.CTkLabel(window, text="Paste a YouTube link:", font=("Arial", 14))
label.pack(pady=(10, 6))

input_link = ctk.CTkEntry(window, width=360)
input_link.pack(pady=(0, 14))

status_var = ctk.StringVar(value="Idle")
status = ctk.CTkLabel(window, textvariable=status_var, font=("Arial", 13))
status.pack(pady=(8, 14))

btn_info = ctk.CTkButton(window, text="Get Video Info", corner_radius=16)
btn_info.pack(pady=(8, 10))

btn_download = ctk.CTkButton(
    window,
    text="Download Max 1080p",
    corner_radius=16,
    fg_color="#D99711",
    hover_color="#704E09"
)
btn_download.pack(pady=(6, 14))


def safe_filename(name: str, max_len: int = 120) -> str:
    name = name.strip()
    name = re.sub(r'[\\/:*?"<>|]+', "_", name)
    name = re.sub(r"\s+", " ", name)
    name = name.strip(" ._")
    return (name[:max_len] or "video")


def ffmpeg_available() -> bool:
    try:
        subprocess.run([FFMPEG_PATH, "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except Exception:
        return False


def set_busy(busy: bool):
    state = "disabled" if busy else "normal"
    btn_info.configure(state=state)
    btn_download.configure(state=state)
    input_link.configure(state=state)


def pick_streams_max_1080(yt: YouTube):
    video = (
        yt.streams
        .filter(only_video=True)
        .filter(resolution=lambda r: r and int(r.replace("p", "")) <= 1080)
        .order_by("resolution")
        .desc()
        .first()
    )

    audio = (
        yt.streams
        .filter(only_audio=True, mime_type="audio/mp4")
        .order_by("abr")
        .desc()
        .first()
    )

    if not audio:
        audio = (
            yt.streams
            .filter(only_audio=True)
            .order_by("abr")
            .desc()
            .first()
        )

    return video, audio


def show_info():
    url = input_link.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a link.")
        return
    try:
        yt = YouTube(url)
        duration = str(timedelta(seconds=yt.length))
        messagebox.showinfo("Video Info", f"Title: {yt.title}\nDuration: {duration}\nAuthor: {yt.author}\nViews: {yt.views}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def merge(video_path, audio_path, out_path, audio_stream):
    mime = audio_stream.mime_type or ""
    codecs = " ".join(audio_stream.codecs or [])

    if "opus" in codecs.lower() or "webm" in mime:
        cmd = [
            FFMPEG_PATH, "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            out_path
        ]
    else:
        cmd = [
            FFMPEG_PATH, "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c", "copy",
            out_path
        ]

    subprocess.run(cmd, check=True)


def download_max_1080():
    url = input_link.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a link.")
        return

    if not ffmpeg_available():
        messagebox.showerror("Error", "ffmpeg not found.")
        return

    def worker():
        try:
            window.after(0, lambda: set_busy(True))
            window.after(0, lambda: status_var.set("Fetching video info..."))

            yt = YouTube(url)
            duration = str(timedelta(seconds=yt.length))

            ok = messagebox.askokcancel(
                "Confirm Download",
                f"Title: {yt.title}\nDuration: {duration}\n\nDownload max 1080p?"
            )
            if not ok:
                window.after(0, lambda: status_var.set("Canceled"))
                return

            video, audio = pick_streams_max_1080(yt)
            if not video or not audio:
                messagebox.showerror("Error", "No suitable streams found.")
                return

            out_dir = os.path.join(os.getcwd(), "downloads")
            os.makedirs(out_dir, exist_ok=True)

            base = safe_filename(yt.title)

            window.after(0, lambda: status_var.set(f"Downloading video ({video.resolution})"))
            video_path = video.download(output_path=out_dir, filename=f"{base}__video")

            window.after(0, lambda: status_var.set(f"Downloading audio ({audio.abr})"))
            audio_path = audio.download(output_path=out_dir, filename=f"{base}__audio")

            window.after(0, lambda: status_var.set("Merging"))
            out_path = os.path.join(out_dir, f"{base}.mp4")

            merge(video_path, audio_path, out_path, audio)

            try:
                os.remove(video_path)
                os.remove(audio_path)
            except Exception:
                pass

            window.after(0, lambda: status_var.set("Done"))
            messagebox.showinfo("Success", f"Saved to:\n{out_path}")

        except Exception as e:
            window.after(0, lambda: status_var.set("Error"))
            messagebox.showerror("Error", str(e))
        finally:
            window.after(0, lambda: set_busy(False))

    threading.Thread(target=worker, daemon=True).start()


btn_info.configure(command=show_info)
btn_download.configure(command=download_max_1080)

window.mainloop()
