import os

lock_file_path = "/home/laurens/Somtoday_Agendas/.git/index.lock"
head_file_path = "/home/laurens/Somtoday_Agendas/.git/HEAD.lock"
if os.path.exists(lock_file_path):
    os.remove(lock_file_path)
elif os.path.exists(head_file_path):
    os.remove(head_file_path)
