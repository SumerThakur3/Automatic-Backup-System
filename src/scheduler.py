import threading
import queue
import time

class FIFOScheduler:

    def __init__(self, backup_engine, gui_callback=None):

        self.processing_files = set()
        self.task_queue = queue.Queue()
        self.backup_engine = backup_engine
        self.running = False
        self.paused = False
        self.gui_callback = gui_callback

    def add_task(self, filepath, source_root):

        if filepath in self.processing_files:
            return

        self.processing_files.add(filepath)

        self.task_queue.put((filepath, source_root))

    def start(self):

        self.running = True

        threading.Thread(
            target=self.process_queue,
            daemon=True
        ).start()

    def process_queue(self):

        while self.running:

            if self.paused:
                time.sleep(1)
                continue

            try:

                filepath, source_root = self.task_queue.get(timeout=1)

                result = self.backup_engine.backup_file(
                    filepath,
                    source_root
                )

                if result and result != "DUPLICATE" and self.gui_callback:
                    self.gui_callback(result)

                self.task_queue.task_done()

                if filepath in self.processing_files:
                    self.processing_files.remove(filepath)

            except queue.Empty:
                continue

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.running = False

    def queue_size(self):
        return self.task_queue.qsize()