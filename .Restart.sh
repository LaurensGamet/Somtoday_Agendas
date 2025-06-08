echo Test

sudo -u www-data sudo tmux kill-session -t Somtoday_Agendas && echo test2

sudo -u www-data sudo bash /home/laurens/Somtoday_Agendas/.Autostart.sh && echo test3

sudo -u www-data sudo tmux send-keys -t Combined_View:0.0 "sudo tmux a -t Somtoday_Agendas" C-m
