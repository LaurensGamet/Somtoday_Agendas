tmux new -d -s Somtoday_Agendas -n Laurens
tmux new-window -t Somtoday_Agendas:1 -n Madelief
tmux new-window -t Somtoday_Agendas:2 -n httpserver
tmux new-window -t Somtoday_Agendas:3 -n autologggitupdater
tmux split-window -h -t Somtoday_Agendas:0
tmux split-window -v -t Somtoday_Agendas:0.0
tmux split-window -v -t Somtoday_Agendas:0.1
tmux select-layout -t Somtoday_Agendas:0 tiled
tmux kill-window -t Somtoday_Agendas:1
tmux kill-window -t Somtoday_Agendas:2


tmux send-keys -t Somtoday_Agendas:0.0 "clear" C-m 
tmux send-keys -t Somtoday_Agendas:0.0 "cd /home/laurens/Somtoday_Agendas/Logs/.LogChecker/Checkers" C-m 
tmux send-keys -t Somtoday_Agendas:0.0 "sudo python3 Somtoday_Laurens.py" C-m

tmux send-keys -t Somtoday_Agendas:0.1 "clear" C-m 
tmux send-keys -t Somtoday_Agendas:0.1 "cd /home/laurens/Somtoday_Agendas/Logs/.LogChecker/Checkers" C-m 
tmux send-keys -t Somtoday_Agendas:0.1 "sudo python3 Somtoday_Madelief.py" C-m

tmux send-keys -t Somtoday_Agendas:0.2 "clear" C-m
tmux send-keys -t Somtoday_Agendas:0.2 "cd /home/laurens/Somtoday_Agendas/Logs/" C-m
tmux send-keys -t Somtoday_Agendas:0.2 "sudo python3 -m http.server" C-m

tmux send-keys -t Somtoday_Agendas:0.3 "clear" C-m
tmux send-keys -t Somtoday_Agendas:0.3 "cd /home/laurens/Somtoday_Agendas/Logs" C-m
tmux send-keys -t Somtoday_Agendas:0.3 "sudo python3 .autoupdategit.py" C-m

