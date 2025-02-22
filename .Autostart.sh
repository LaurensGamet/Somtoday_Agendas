tmux new -d -s Somtoday_Agendas -n Laurens
tmux split-window -h -t Somtoday_Agendas:0
tmux split-window -v -t Somtoday_Agendas:0.0
tmux split-window -v -t Somtoday_Agendas:0.1
tmux select-layout -t Somtoday_Agendas:0 tiled


tmux send-keys -t Somtoday_Agendas:0.0 "sudo python3 /home/laurens/Somtoday_Agendas/Logs/.Checkers/Somtoday_Laurens.py" C-m

tmux send-keys -t Somtoday_Agendas:0.1 "sudo python3 /home/laurens/Somtoday_Agendas/Logs/.Checkers/Somtoday_Madelief.py" C-m 

tmux send-keys -t Somtoday_Agendas:0.2 "cd /home/laurens/Somtoday_Agendas/Logs/" C-m
tmux send-keys -t Somtoday_Agendas:0.2 "sudo python3 -m http.server 80" C-m

tmux send-keys -t Somtoday_Agendas:0.3 "sudo python3 /home/laurens/Somtoday_Agendas/.autoupdategit.py" C-m

sleep 15

sudo bash /home/laurens/Somtoday_Agendas/.run-updater.sh
