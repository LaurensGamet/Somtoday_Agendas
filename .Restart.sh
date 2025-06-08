#!/bin/bash

whoami
echo Test

# Kill old session if it exists
tmux has-session -t Somtoday_Agendas 2>/dev/null
if [ $? -eq 0 ]; then
    tmux kill-session -t Somtoday_Agendas && echo test2
else
    echo "No existing Somtoday_Agendas session"
fi

# Start the session using .Autostart.sh
bash /home/laurens/Somtoday_Agendas/.Autostart.sh && echo test3

# Wait a moment for tmux session to start
sleep 1

sudo -u root tmux ls

# Send command to the session (adjust session name if needed)
if tmux has-session -t Combined_View 2>/dev/null; then
    tmux send-keys -t Combined_View:0.0 "tmux attach -t Somtoday_Agendas" C-m
else
    echo "⚠️ Session Combined_View not found."
fi
