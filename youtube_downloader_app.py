import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import yt_dlp
import threading
import requests
from io import BytesIO
import os

FFMPEG_PATH = r"C:\Users\Ricky\Downloads\ffmpeg-8.1.2-essentials_build\ffmpeg-8.1.2-essentials_build\bin"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class YouTubeDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ProTube Downloader")
        self.geometry("900x760")
        self.resizable(False, False)
        self.configure(fg_color="#121212")

        self.folder = os.path.join(os.path.expanduser("~"), "Downloads")
        self.thumbnail_image = None
        self.video_data = None

        self.main_frame = ctk.CTkFrame(self, fg_color="#121212")
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Header
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="🎬 ProTube",
            font=("Segoe UI", 36, "bold"),
            text_color="white"
        )
        self.title_label.pack(pady=(5, 0))

        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Professional YouTube Downloader",
            font=("Segoe UI", 14),
            text_color="#B3B3B3"
        )
        self.subtitle_label.pack(pady=(0, 20))

        # URL card
        self.url_card = ctk.CTkFrame(
            self.main_frame,
            fg_color="#1E1E1E",
            corner_radius=18
        )
        self.url_card.pack(fill="x", padx=5, pady=10)

        self.url_label = ctk.CTkLabel(
            self.url_card,
            text="Paste YouTube Link",
            font=("Segoe UI", 15, "bold"),
            text_color="white"
        )
        self.url_label.pack(anchor="w", padx=22, pady=(18, 6))

        self.url_entry = ctk.CTkEntry(
            self.url_card,
            width=790,
            height=42,
            placeholder_text="https://youtube.com/watch?v=...",
            fg_color="#2A2A2A",
            border_color="#333333",
            text_color="white"
        )
        self.url_entry.pack(padx=22, pady=(0, 14))

        self.folder_label = ctk.CTkLabel(
            self.url_card,
            text=f"Save to: {self.folder}",
            wraplength=780,
            font=("Segoe UI", 12),
            text_color="#B3B3B3"
        )
        self.folder_label.pack(padx=22, pady=(0, 12))

        self.top_button_frame = ctk.CTkFrame(self.url_card, fg_color="transparent")
        self.top_button_frame.pack(pady=(0, 20))

        self.folder_button = ctk.CTkButton(
            self.top_button_frame,
            text="📁 Choose Folder",
            width=180,
            height=38,
            fg_color="#333333",
            hover_color="#444444",
            command=self.choose_folder
        )
        self.folder_button.grid(row=0, column=0, padx=8)

        self.analyze_button = ctk.CTkButton(
            self.top_button_frame,
            text="🔍 Analyze Video",
            width=180,
            height=38,
            fg_color="#1DB954",
            hover_color="#169C46",
            text_color="black",
            font=("Segoe UI", 13, "bold"),
            command=self.start_analyze
        )
        self.analyze_button.grid(row=0, column=1, padx=8)

        # Video info card
        self.info_card = ctk.CTkFrame(
            self.main_frame,
            fg_color="#1E1E1E",
            corner_radius=18
        )
        self.info_card.pack(fill="x", padx=5, pady=10)

        self.info_content = ctk.CTkFrame(self.info_card, fg_color="transparent")
        self.info_content.pack(fill="x", padx=20, pady=20)

        self.thumbnail_label = ctk.CTkLabel(
            self.info_content,
            text="No Thumbnail",
            width=260,
            height=145,
            fg_color="#2A2A2A",
            corner_radius=12,
            text_color="#B3B3B3"
        )
        self.thumbnail_label.grid(row=0, column=0, rowspan=5, padx=(0, 22))

        self.video_title = ctk.CTkLabel(
            self.info_content,
            text="No video analyzed yet",
            font=("Segoe UI", 20, "bold"),
            text_color="white",
            wraplength=520,
            justify="left"
        )
        self.video_title.grid(row=0, column=1, sticky="w", pady=(5, 5))

        self.video_channel = ctk.CTkLabel(
            self.info_content,
            text="Channel: —",
            font=("Segoe UI", 14),
            text_color="#B3B3B3"
        )
        self.video_channel.grid(row=1, column=1, sticky="w", pady=3)

        self.video_duration = ctk.CTkLabel(
            self.info_content,
            text="Duration: —",
            font=("Segoe UI", 14),
            text_color="#B3B3B3"
        )
        self.video_duration.grid(row=2, column=1, sticky="w", pady=3)

        self.video_views = ctk.CTkLabel(
            self.info_content,
            text="Views: —",
            font=("Segoe UI", 14),
            text_color="#B3B3B3"
        )
        self.video_views.grid(row=3, column=1, sticky="w", pady=3)

        self.video_status = ctk.CTkLabel(
            self.info_content,
            text="Paste a link and click Analyze Video.",
            font=("Segoe UI", 13),
            text_color="#777777"
        )
        self.video_status.grid(row=4, column=1, sticky="w", pady=(12, 0))

        # Download card
        self.download_card = ctk.CTkFrame(
            self.main_frame,
            fg_color="#1E1E1E",
            corner_radius=18
        )
        self.download_card.pack(fill="x", padx=5, pady=10)

        self.download_button = ctk.CTkButton(
            self.download_card,
            text="⬇ Download MP4",
            width=220,
            height=42,
            fg_color="#1DB954",
            hover_color="#169C46",
            text_color="black",
            font=("Segoe UI", 15, "bold"),
            command=self.start_download
        )
        self.download_button.pack(pady=(20, 10))

        self.status = ctk.CTkLabel(
            self.download_card,
            text="Ready",
            font=("Segoe UI", 14),
            text_color="#B3B3B3"
        )
        self.status.pack(pady=(5, 8))

        self.progress = ctk.CTkProgressBar(
            self.download_card,
            width=790,
            height=14,
            progress_color="#1DB954",
            fg_color="#333333"
        )
        self.progress.set(0)
        self.progress.pack(pady=(0, 20))

        self.footer = ctk.CTkLabel(
            self.main_frame,
            text="Use only for videos you own or have permission to download.",
            font=("Segoe UI", 11),
            text_color="#777777"
        )
        self.footer.pack(pady=(5, 0))

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder = folder
            self.folder_label.configure(text=f"Save to: {self.folder}")

    def format_duration(self, seconds):
        if not seconds:
            return "Unknown"

        seconds = int(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"

        return f"{minutes}:{secs:02d}"

    def format_views(self, views):
        if not views:
            return "Unknown"

        if views >= 1_000_000:
            return f"{views / 1_000_000:.1f}M views"

        if views >= 1_000:
            return f"{views / 1_000:.1f}K views"

        return f"{views} views"

    def start_analyze(self):
        thread = threading.Thread(target=self.analyze_video)
        thread.daemon = True
        thread.start()

    def analyze_video(self):
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showerror("Error", "Please paste a YouTube link.")
            return

        try:
            self.analyze_button.configure(state="disabled", text="Analyzing...")
            self.video_status.configure(text="Getting video information...")

            options = {
                "quiet": True,
                "skip_download": True,
                "noplaylist": True,
            }

            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)

            self.video_data = info

            title = info.get("title", "Unknown Title")
            channel = info.get("uploader") or info.get("channel") or "Unknown Channel"
            duration = self.format_duration(info.get("duration"))
            views = self.format_views(info.get("view_count"))
            thumbnail_url = info.get("thumbnail")

            self.video_title.configure(text=title)
            self.video_channel.configure(text=f"Channel: {channel}")
            self.video_duration.configure(text=f"Duration: {duration}")
            self.video_views.configure(text=f"Views: {views}")
            self.video_status.configure(text="Video analyzed successfully ✅")

            if thumbnail_url:
                response = requests.get(thumbnail_url, timeout=10)
                image = Image.open(BytesIO(response.content))
                image = image.resize((260, 145))

                self.thumbnail_image = ctk.CTkImage(
                    light_image=image,
                    dark_image=image,
                    size=(260, 145)
                )

                self.thumbnail_label.configure(
                    image=self.thumbnail_image,
                    text=""
                )

        except Exception as e:
            self.video_status.configure(text="Analyze failed.")
            messagebox.showerror("Error", str(e))

        finally:
            self.analyze_button.configure(state="normal", text="🔍 Analyze Video")

    def progress_hook(self, data):
        if data.get("status") == "downloading":
            percent = data.get("_percent_str", "0%").replace("%", "").strip()

            try:
                number = float(percent)
                self.progress.set(number / 100)
                self.status.configure(text=f"Downloading... {percent}%")
            except:
                self.status.configure(text="Downloading...")

        elif data.get("status") == "finished":
            self.status.configure(text="Finalizing MP4...")
            self.progress.set(1)

    def start_download(self):
        thread = threading.Thread(target=self.download_video)
        thread.daemon = True
        thread.start()

    def download_video(self):
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showerror("Error", "Please paste a YouTube link.")
            return

        try:
            self.download_button.configure(state="disabled", text="Downloading...")
            self.status.configure(text="Starting download...")
            self.progress.set(0)

            options = {
                "format": "bv*[vcodec^=avc1][height<=1080]+ba/b[ext=mp4]/best",
                "outtmpl": os.path.join(self.folder, "%(title)s.%(ext)s"),
                "merge_output_format": "mp4",
                "ffmpeg_location": FFMPEG_PATH,
                "postprocessor_args": [
                    "-c:v", "copy",
                    "-c:a", "aac",
                    "-b:a", "192k"
                ],
                "progress_hooks": [self.progress_hook],
                "noplaylist": True,
            }

            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([url])

            self.status.configure(text="Download complete!")
            messagebox.showinfo("Done", "Video downloaded successfully.")

        except Exception as e:
            self.status.configure(text="Download failed.")
            messagebox.showerror("Error", str(e))

        finally:
            self.download_button.configure(state="normal", text="⬇ Download MP4")


app = YouTubeDownloader()
app.mainloop()