import os

lock_file_path = "/home/laurens/Somtoday_Agendas/.git/index.lock"
if os.path.exists(lock_file_path):
    os.remove(lock_file_path)