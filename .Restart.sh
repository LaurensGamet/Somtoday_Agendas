#!/bin/bash

# Kill Somtoday_Agendas if it exists
if tmux has-session -t Somtoday_Agendas 2>/dev/null; then
    tmux kill-session -t Somtoday_Agendas && echo "✅ Killed Somtoday_Agendas"
else
    echo "ℹ️ No existing Somtoday_Agendas session"
fi

# Start the session using Autostart script
bash /home/laurens/Somtoday_Agendas/.Autostart.sh && echo "✅ Ran Autostart"

# Wait for Somtoday_Agendas session to appear (up to 5 seconds)
for i in {1..5}; do
    if tmux has-session -t Somtoday_Agendas 2>/dev/null; then
        break
    fi
    sleep 1
done

# Send attach command to Combined_View session if it exists
if tmux has-session -t Combined_View 2>/dev/null; then
    tmux send-keys -t Combined_View:0.0 "tmux attach -t Somtoday_Agendas" C-m
    # Confirm the session here: is Discord_Bots the right target for layout?
    tmux select-layout -t Discord_Bots:0 tiled
    echo "✅ Sent attach command to Combined_View"
else
    echo "⚠️ Session Combined_View not found"
fi
