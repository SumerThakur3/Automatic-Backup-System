import customtkinter as ctk
from tkinter import filedialog
import json
import os
from datetime import datetime

from src.monitor import FolderMonitor
from src.scheduler import FIFOScheduler
from src.backup_engine import BackupEngine

SETTINGS_FILE = "config/settings.json"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BackupGUI:

    def __init__(self):

        self.root = ctk.CTk()

        self.root.title("Automatic Backup System")

        self.root.geometry("1000x700")

        self.source_folders = []
        self.backup_folder = ""

        self.load_settings()

        self.setup_ui()

        self.backup_engine = BackupEngine(
            self.backup_folder
        )

        self.scheduler = FIFOScheduler(
            self.backup_engine,
            self.update_logs
        )

        self.monitor = FolderMonitor(
            self.scheduler
        )

    def setup_ui(self):

        title = ctk.CTkLabel(
            self.root,
            text="REAL-TIME AUTOMATIC BACKUP SYSTEM",
            font=("Arial", 24, "bold")
        )

        title.pack(pady=20)

        self.log_box = ctk.CTkTextbox(
            self.root,
            width=900,
            height=350
        )

        self.log_box.pack(pady=20)

        button_frame = ctk.CTkFrame(self.root)

        button_frame.pack(pady=20)

        ctk.CTkButton(
            button_frame,
            text="Select Source Folder",
            command=self.select_source_folder
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            button_frame,
            text="Select Backup Folder",
            command=self.select_backup_folder
        ).grid(row=0, column=1, padx=10)

        ctk.CTkButton(
            button_frame,
            text="Start",
            command=self.start_backup
        ).grid(row=1, column=0, pady=10)

        ctk.CTkButton(
            button_frame,
            text="Pause",
            command=self.pause_backup
        ).grid(row=1, column=1)

        ctk.CTkButton(
            button_frame,
            text="Resume",
            command=self.resume_backup
        ).grid(row=1, column=2)

        ctk.CTkButton(
            button_frame,
            text="Stop",
            fg_color="red",
            command=self.stop_backup
        ).grid(row=1, column=3)

        self.status_label = ctk.CTkLabel(
            self.root,
            text="Status: Idle"
        )

        self.status_label.pack(pady=10)

        self.queue_label = ctk.CTkLabel(
            self.root,
            text="Queue Size: 0"
        )

        self.queue_label.pack()

    def update_logs(self, message):

        timestamp = datetime.now().strftime("%H:%M:%S")

        self.log_box.insert(
            "end",
            f"[{timestamp}] {message}\n"
        )

        self.log_box.see("end")

        self.queue_label.configure(
            text=f"Queue Size: {self.scheduler.queue_size()}"
        )

    def select_source_folder(self):

        folder = filedialog.askdirectory()

        if folder:
            self.source_folders.append(folder)

            self.update_logs(
                f"Added source folder: {folder}"
            )

            self.save_settings()

    def select_backup_folder(self):

        folder = filedialog.askdirectory()

        if folder:
            self.backup_folder = folder

            self.update_logs(
                f"Backup folder selected: {folder}"
            )

            self.save_settings()

    def start_backup(self):

        if not self.source_folders:
            self.update_logs("No source folders selected")
            return

        if not self.backup_folder:
            self.update_logs("No backup folder selected")
            return

        self.backup_engine = BackupEngine(
            self.backup_folder
        )

        self.scheduler = FIFOScheduler(
            self.backup_engine,
            self.update_logs
        )

        self.monitor = FolderMonitor(
            self.scheduler
        )

        self.scheduler.start()

        self.monitor.start_monitoring(
            self.source_folders
        )

        self.status_label.configure(
            text="Status: Running"
        )

        self.update_logs(
            "Backup service started successfully"
        )

    def pause_backup(self):

        self.scheduler.pause()

        self.status_label.configure(
            text="Status: Paused"
        )

        self.update_logs(
            "Backup paused"
        )

    def resume_backup(self):

        self.scheduler.resume()

        self.status_label.configure(
            text="Status: Running"
        )

        self.update_logs(
            "Backup resumed"
        )

    def stop_backup(self):

        self.scheduler.stop()

        self.monitor.stop_monitoring()

        self.status_label.configure(
            text="Status: Stopped"
        )

        self.update_logs(
            "Backup stopped"
        )

    def save_settings(self):

        data = {
            "source_folders": self.source_folders,
            "backup_folder": self.backup_folder
        }

        with open(SETTINGS_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load_settings(self):

        if os.path.exists(SETTINGS_FILE):

            with open(SETTINGS_FILE, "r") as f:

                data = json.load(f)

                self.source_folders = data.get(
                    "source_folders",
                    []
                )

                self.backup_folder = data.get(
                    "backup_folder",
                    ""
                )

    def run(self):
        self.root.mainloop()