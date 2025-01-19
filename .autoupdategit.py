import subprocess
import time
from datetime import datetime


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


# Run the update every 2 minutes
if __name__ == "__main__":
    print("Starting Git repository auto-updater. Press Ctrl+C to stop.\n")
    try:
        while True:
            update_git_repo()
            print("Waiting for 2 minutes...\n")
            time.sleep(120)  # Wait for 120 seconds
    except KeyboardInterrupt:
        print("Updater stopped.")
