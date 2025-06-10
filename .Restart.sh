#!/bin/bash

# Define tmux socket path
TMUX_SOCKET="/tmp/tmux-0/default"

echo "Running as: $(whoami)"
echo "Using TMUX socket: $TMUX_SOCKET"
echo "Test"

# Kill Somtoday_Agendas if it exists
tmux -S "$TMUX_SOCKET" has-session -t Somtoday_Agendas 2>/dev/null
if [ $? -eq 0 ]; then
    tmux -S "$TMUX_SOCKET" kill-session -t Somtoday_Agendas && echo "✅ Killed Somtoday_Agendas"
else
    echo "ℹ️ No existing Somtoday_Agendas session"
fi

# Start the session using Autostart
bash /home/laurens/Somtoday_Agendas/.Autostart.sh && echo "✅ Ran Autostart"

# Wait for tmux to initialize session
sleep 1

# Show available sessions
echo "🔍 Available tmux sessions:"
tmux -S "$TMUX_SOCKET" ls

# Send command to Combined_View if it exists
if tmux -S "$TMUX_SOCKET" has-session -t Combined_View 2>/dev/null; then
    tmux -S "$TMUX_SOCKET" send-keys -t Combined_View:0.0 "tmux attach -t Somtoday_Agendas" C-m
    tmux -S "$TMUX_SOCKET" select-layout -t Discord_Bots:0 tiled
    echo "✅ Sent attach command to Combined_View"
else
    echo "⚠️ Session Combined_View not found"
fi
