import subprocess
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Function to execute a Git command and handle errors
def run_git_command(command):
    try:
        result = subprocess.run(
            command,
            check=True,
            text=True,
            capture_output=True
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
    run_git_command(["git", "add", "."])
    
    # Check for changes to commit
    status_output = run_git_command(["git", "status", "--porcelain"])
    if status_output:
        print("Changes detected. Preparing to commit...")
        
        # Create commit message with the current date and time
        now = datetime.now()
        commit_message = now.strftime("%H%M%d%m%Y")  # Format: HHMMDDMMYYYY
        
        # Commit changes
        commit_output = run_git_command(["git", "commit", "-m", commit_message])
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

    def on_any_event(self, event):
        current_time = time.time()
        if current_time - self.last_run >= 60:  # Ensure at least 1 minute between updates
            self.last_run = current_time
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
