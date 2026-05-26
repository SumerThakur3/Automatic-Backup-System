from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os


class FileMonitorHandler(FileSystemEventHandler):

    def __init__(self, scheduler, source_root):

        self.scheduler = scheduler
        self.source_root = source_root

    def should_ignore(self, filepath):

        filename = os.path.basename(filepath)

        ignored_extensions = (
            ".crdownload",
            ".tmp",
            ".part",
            ".download"
        )

        # Ignore Office temp files
        if filename.startswith("~$"):
            return True

        # Ignore hidden files
        if filename.startswith("."):
            return True

        # Ignore temporary downloads
        if filename.endswith(ignored_extensions):
            return True

        return False

    def on_created(self, event):

        if not event.is_directory:

            if self.should_ignore(event.src_path):
                return

            self.scheduler.add_task(
                event.src_path,
                self.source_root
            )

    def on_modified(self, event):

        if not event.is_directory:

            if self.should_ignore(event.src_path):
                return

            self.scheduler.add_task(
                event.src_path,
                self.source_root
            )


class FolderMonitor:

    def __init__(self, scheduler):

        self.scheduler = scheduler
        self.observers = []

    def start_monitoring(self, folders):

        for folder in folders:

            event_handler = FileMonitorHandler(
                self.scheduler,
                folder
            )

            observer = Observer()

            observer.schedule(
                event_handler,
                folder,
                recursive=True
            )

            observer.start()

            self.observers.append(observer)

    def stop_monitoring(self):

        for observer in self.observers:
            observer.stop()
            observer.join()