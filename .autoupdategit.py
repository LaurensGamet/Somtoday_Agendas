import subprocess
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

# Path to the Git repository
GIT_REPO_PATH = "/home/laurens/Somtoday_Agendas/"

# Function to execute a Git command and handle errors
def run_git_command(command):
    try:
        result = subprocess.run(
            command,
            check=True,
            text=True,
            capture_output=True,
            cwd=GIT_REPO_PATH  # Ensure commands are executed in the correct repository
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(command)}:")
        print(e.stderr.strip())
        return None

# Function to pull, commit, and push updates
def update_git_repo():
    print(f"Updating Git repository...\n")
    
    # Pull updates
    pull_output = run_git_command(["git", "pull"])
    if pull_output:
        print(f"Git pull output:\n{pull_output}\n")
    
    # Stage all changes
    run_git_command(["git", "add", "--ignore-errors", "."])
    
    # Check for changes to commit
    status_output = run_git_command(["git", "status", "--porcelain"])
    if status_output:
        print(f"Changes detected. Preparing to commit...")
        
        # Create commit message with the current date and time
        now = datetime.now()
        commit_message = now.strftime("%H.%M %d-%m-%Y")  # Format: HH.MM DD-MM-YYYY
        
        # Commit changes
        commit_output = run_git_command(["git", "commit", "--allow-empty", "-m", commit_message])
        if commit_output:
            print(f"Commit successful:\n{commit_output}\n")
        
        # Push changes
        push_output = run_git_command(["git", "push"])
        if push_output:
            print(f"Push successful:\n{push_output}\n")
    else:
        print(f"No changes to commit.\n")

# Define a custom event handler for folder changes
class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.last_run = 0  # Timestamp of the last update

    def is_in_git_folder(self, path):
        """ Check if the event is inside the .git folder """
        return '.git' in path

    def on_modified(self, event):
        if not event.is_directory and not self.is_in_git_folder(event.src_path):  # Ignore changes in .git folder
            current_time = time.time()
            if current_time - self.last_run >= 120:  # Ensure at least 1 minute between updates
                print(f"Change detected in file: {event.src_path}")
                self.last_run = current_time
                time.sleep(15)
                update_git_repo()
                time.sleep(60)  # Wait for 1 minute and then recheck for changes
                update_git_repo()

    def on_created(self, event):
        if not event.is_directory and not self.is_in_git_folder(event.src_path):  # Ignore creations in .git folder
            current_time = time.time()
            if current_time - self.last_run >= 120:  # Ensure at least 1 minute between updates
                print(f"File created: {event.src_path}")
                self.last_run = current_time
                time.sleep(20)
                update_git_repo()
                time.sleep(60)  # Wait for 1 minute and then recheck for changes
                update_git_repo()

# Main function to set up folder monitoring
if __name__ == "__main__":
    FOLDER_TO_WATCH = "/home/laurens/Somtoday_Agendas/"

    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=FOLDER_TO_WATCH, recursive=True)
    
    try:
        print(f"Monitoring changes in {FOLDER_TO_WATCH}...")
        observer.start()
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        print("Stopping the observer.")
        observer.stop()
    observer.join()
