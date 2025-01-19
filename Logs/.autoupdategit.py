import time
import subprocess
import os
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LogFileHandler(FileSystemEventHandler):
    def __init__(self, files_to_monitor):
        self.files_to_monitor = files_to_monitor
        self.last_modified = {}

    def on_modified(self, event):
        for file_path in self.files_to_monitor:
            if event.src_path.endswith(file_path):
                current_mtime = os.path.getmtime(file_path)
                if self.last_modified.get(file_path) != current_mtime:
                    self.last_modified[file_path] = current_mtime
                    print(f"\n{file_path} has been modified. Committing changes.")
                    self.commit_and_push_changes(file_path)

    def commit_and_push_changes(self, file_path):
        try:
            # Stage the file
            subprocess.run(["git", "add", file_path], check=True)

            # Check for staged changes
            diff_check = subprocess.run(["git", "diff", "--cached", "--exit-code"], capture_output=True)
            if diff_check.returncode != 0:
                current_datetime = datetime.now().strftime("%H%M%d%m%Y")
                commit_message = f"{current_datetime}"

                # Commit and push changes
                subprocess.run(["git", "commit", "-m", commit_message], check=True)
                subprocess.run(["git", "push"], check=True)
                print(f"Changes pushed successfully for {file_path} with message '{commit_message}'.")
            else:
                print(f"No changes to commit for {file_path}.")
        except subprocess.CalledProcessError as e:
            print(f"Error during Git operation for {file_path}: {e}")

def monitor_log_files(files_to_monitor):
    event_handler = LogFileHandler(files_to_monitor)
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    log_files = ["Somtoday_Laurens.log", "Somtoday_Madelief.log"]
    monitor_log_files(log_files)