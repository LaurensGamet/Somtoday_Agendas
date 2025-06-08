echo Test

sudo -u www-data sudo tmux kill-session -t Somtoday_Agendas

sudo -u www-data sudo bash /home/laurens/Somtoday_Agendas/.Autostart.sh

sudo -u www-data sudo tmux send-keys -t Combined_View:0.0 "sudo tmux a -t Somtoday_Agendas" C-m
