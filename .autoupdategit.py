import time
import subprocess
import os
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LogFileHandler(FileSystemEventHandler):
    def __init__(self, directories_to_monitor):
        self.directories_to_monitor = directories_to_monitor
        self.last_modified = {}

    def on_modified(self, event):
        if event.is_directory:
            return  # Ignore directory-level modifications

        file_path = event.src_path
        if any(file_path.startswith(directory) for directory in self.directories_to_monitor):
            current_mtime = os.path.getmtime(file_path)
            if self.last_modified.get(file_path) != current_mtime:
                self.last_modified[file_path] = current_mtime
                print(f"\n{file_path} has been modified. Committing changes.")
                self.commit_and_push_changes(file_path)

    def commit_and_push_changes(self, file_path):
        try:
            # Ensure local repository is up to date
            print("Fetching and pulling latest changes...")
            subprocess.run(["git", "fetch"], check=True)
            subprocess.run(["git", "pull", "--rebase"], check=True)

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
            print("\nAttempting to stash changes...")
            self.stash_changes()

    def stash_changes(self):
        try:
            # Stash local changes to avoid conflicts
            subprocess.run(["git", "stash", "push", "-m", "Auto-stash before pull"], check=True)

            # Pull latest changes after stashing
            subprocess.run(["git", "pull", "--rebase"], check=True)

            # Apply stashed changes
            subprocess.run(["git", "stash", "pop"], check=True)
            print("Stashed changes applied successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error during stashing process: {e}")

def monitor_directories(directories_to_monitor):
    event_handler = LogFileHandler(directories_to_monitor)
    observer = Observer()
    for directory in directories_to_monitor:
        observer.schedule(event_handler, directory, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # Specify directories to monitor
    directories = ["/home/laurens/Somtoday_Agendas/Laurens", "/home/laurens/Somtoday_Agendas/Madelief", "/home/laurens/Somtoday_Agendas/Logs"]
    monitor_directories(directories)
