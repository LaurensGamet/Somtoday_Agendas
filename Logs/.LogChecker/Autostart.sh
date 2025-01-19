tmux new -d -s Somtoday_Laurens
tmux send-keys -t Somtoday_Laurens "clear" C-m 
tmux send-keys -t Somtoday_Laurens "cd /home/laurens/Somtoday_Agendas/Logs/.LogChecker/Checkers" C-m 
tmux send-keys -t Somtoday_Laurens "sudo python3 Somtoday_Laurens.py" C-m
tmux new -d -s Somtoday_Madelief
tmux send-keys -t Somtoday_Madelief "clear" C-m 
tmux send-keys -t Somtoday_Madelief "cd /home/laurens/Somtoday_Agendas/Logs/.LogChecker/Checkers" C-m 
tmux send-keys -t Somtoday_Madelief "sudo python3 Somtoday_Madelief.py" C-m
tmux new -d -s httpserver
tmux send-keys -t httpserver "clear" C-m
tmux send-keys -t httpserver "cd /home/laurens/Somtoday_Agendas/Logs/" C-m
tmux send-keys -t httpserver "sudo python3 -m http.server" C-m
tmux new -d -s autologgitupdater
tmux send-keys -t autologgitupdater "clear" C-m
tmux send-keys -t autologgitupdater "cd /home/laurens/Somtoday_Agendas/Logs" C-m
tmux send-keys -t autologgitupdater "sudo python3 .autoupdategit.py" C-m

