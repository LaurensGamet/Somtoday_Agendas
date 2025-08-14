import os

lock_file_path = "/home/laurens/Somtoday_Agendas/.git/index.lock"
head_file_path = "/home/laurens/Somtoday_Agendas/.git/HEAD.lock"
#if os.path.exists(lock_file_path):
#    os.remove(lock_file_path)
#elif os.path.exists(head_file_path):
#    os.remove(head_file_path)


try:
    os.remove(lock_file_path)
    print(f"Removed lock file: {lock_file_path}")
except FileNotFoundError:
    print(f"No lock file found at: {lock_file_path} — nothing to remove.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

try:
    os.remove(head_file_path)
    print(f"Removed head file: {head_file_path}")
except FileNotFoundError:
    print(f"No head file found at: {head_file_path} — nothing to remove.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")