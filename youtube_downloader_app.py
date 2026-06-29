import customtkinter as ctk
from tkinter import filedialog, messagebox
import yt_dlp
import threading
import os

FFMPEG_PATH = r"C:\Users\Ricky\Downloads\ffmpeg-8.1.2-essentials_build\ffmpeg-8.1.2-essentials_build\bin"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class YouTubeDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ProTube Downloader")
        self.geometry("700x520")
        self.resizable(False, False)

        self.folder = os.path.join(os.path.expanduser("~"), "Downloads")

        self.configure(fg_color="#121212")

        self.main_frame = ctk.CTkFrame(self, fg_color="#121212")
        self.main_frame.pack(fill="both", expand=True, padx=25, pady=20)

        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="🎬 ProTube",
            font=("Segoe UI", 34, "bold"),
            text_color="white"
        )
        self.title_label.pack(pady=(5, 2))

        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Professional YouTube Downloader",
            font=("Segoe UI", 14),
            text_color="#B3B3B3"
        )
        self.subtitle_label.pack(pady=(0, 20))

        self.card = ctk.CTkFrame(
            self.main_frame,
            fg_color="#1E1E1E",
            corner_radius=18
        )
        self.card.pack(fill="x", padx=10, pady=10)

        self.url_label = ctk.CTkLabel(
            self.card,
            text="Paste YouTube Link",
            font=("Segoe UI", 15, "bold"),
            text_color="white"
        )
        self.url_label.pack(anchor="w", padx=22, pady=(20, 6))

        self.url_entry = ctk.CTkEntry(
            self.card,
            width=590,
            height=42,
            placeholder_text="https://youtube.com/watch?v=...",
            fg_color="#2A2A2A",
            border_color="#333333",
            text_color="white"
        )
        self.url_entry.pack(padx=22, pady=(0, 14))

        self.folder_label = ctk.CTkLabel(
            self.card,
            text=f"Save to: {self.folder}",
            wraplength=580,
            font=("Segoe UI", 12),
            text_color="#B3B3B3"
        )
        self.folder_label.pack(padx=22, pady=(0, 12))

        self.button_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.button_frame.pack(pady=(0, 20))

        self.folder_button = ctk.CTkButton(
            self.button_frame,
            text="📁 Choose Folder",
            width=175,
            height=38,
            fg_color="#333333",
            hover_color="#444444",
            command=self.choose_folder
        )
        self.folder_button.grid(row=0, column=0, padx=8)

        self.download_button = ctk.CTkButton(
            self.button_frame,
            text="⬇ Download MP4",
            width=175,
            height=38,
            fg_color="#1DB954",
            hover_color="#169C46",
            text_color="black",
            font=("Segoe UI", 13, "bold"),
            command=self.start_download
        )
        self.download_button.grid(row=0, column=1, padx=8)

        self.info_card = ctk.CTkFrame(
            self.main_frame,
            fg_color="#1E1E1E",
            corner_radius=18
        )
        self.info_card.pack(fill="x", padx=10, pady=10)

        self.video_title = ctk.CTkLabel(
            self.info_card,
            text="Ready to download",
            font=("Segoe UI", 18, "bold"),
            text_color="white"
        )
        self.video_title.pack(pady=(20, 5))

        self.video_subtitle = ctk.CTkLabel(
            self.info_card,
            text="Paste a link above and click Download MP4.",
            font=("Segoe UI", 13),
            text_color="#B3B3B3"
        )
        self.video_subtitle.pack(pady=(0, 20))

        self.status = ctk.CTkLabel(
            self.main_frame,
            text="Ready",
            font=("Segoe UI", 14),
            text_color="#B3B3B3"
        )
        self.status.pack(pady=(10, 8))

        self.progress = ctk.CTkProgressBar(
            self.main_frame,
            width=610,
            height=14,
            progress_color="#1DB954",
            fg_color="#333333"
        )
        self.progress.set(0)
        self.progress.pack(pady=(0, 10))

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

    def download_video(self):
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showerror("Error", "Please paste a YouTube link.")
            return

        try:
            self.download_button.configure(state="disabled", text="Downloading...")
            self.status.configure(text="Starting download...")
            self.video_title.configure(text="Downloading video...")
            self.video_subtitle.configure(text="Please wait while ProTube prepares your MP4.")
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
            self.video_title.configure(text="Download complete ✅")
            self.video_subtitle.configure(text="Your MP4 video is ready.")
            messagebox.showinfo("Done", "Video downloaded successfully.")

        except Exception as e:
            self.status.configure(text="Download failed.")
            self.video_title.configure(text="Download failed")
            self.video_subtitle.configure(text="Something went wrong. Check the error message.")
            messagebox.showerror("Error", str(e))

        finally:
            self.download_button.configure(state="normal", text="⬇ Download MP4")

    def start_download(self):
        thread = threading.Thread(target=self.download_video)
        thread.daemon = True
        thread.start()


app = YouTubeDownloader()
app.mainloop()