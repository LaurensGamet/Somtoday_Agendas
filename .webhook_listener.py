from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
import os, pty, select, subprocess

app = Flask(__name__)
socketio = SocketIO(app)

VALID_USERNAME = "pi"
VALID_PASSWORD = "raspberry"

# State tracking for login
login_states = {}

@app.route('/')
def index():
    return render_template("redirect_center.html")

# Terminal WebSocket
@socketio.on("connect")
def handle_connect():
    sid = request.sid
    login_states[sid] = {
        "stage": "username",  # or "password" or "authenticated"
        "username": "",
        "shell_pid": None,
        "fd": None
    }
    emit("pty_output", "raspberry login: ")

@socketio.on("pty_input")
def handle_input(data):
    sid = request.sid
    state = login_states.get(sid)

    if not state:
        return

    if state["stage"] == "username":
        state["username"] = data.strip()
        state["stage"] = "password"
        emit("pty_output", "\r\nPassword: ")
    elif state["stage"] == "password":
        if state["username"] == VALID_USERNAME and data.strip() == VALID_PASSWORD:
            state["stage"] = "authenticated"
            pid, fd = pty.fork()
            if pid == 0:
                subprocess.run(["/bin/bash"])
            else:
                state["shell_pid"] = pid
                state["fd"] = fd
                emit("pty_output", "\r\nWelcome to Raspberry Pi!\r\n\n")
        else:
            state["stage"] = "username"
            emit("pty_output", "\r\nLogin incorrect\r\n\nraspberry login: ")
    elif state["stage"] == "authenticated":
        os.write(state["fd"], data.encode())

def read_and_emit():
    while True:
        for sid, state in login_states.items():
            if state.get("fd") and state.get("stage") == "authenticated":
                if select.select([state["fd"]], [], [], 0)[0]:
                    output = os.read(state["fd"], 1024).decode(errors="ignore")
                    socketio.emit("pty_output", output, room=sid)

@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    if sid in login_states:
        if login_states[sid].get("fd"):
            os.close(login_states[sid]["fd"])
        del login_states[sid]

# Script endpoints
@app.route('/reset')     ; def reset(): subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.Reset.sh"])     ; return "Reset", 200
@app.route('/restart')   ; def restart(): subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.Restart.sh"]) ; return "Restart", 200
@app.route('/update')    ; def update(): subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.run-updater.sh"]); return "Update", 200
@app.route('/autostart') ; def auto(): subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.Autostart.sh"])   ; return "Autostart", 200

if __name__ == '__main__':
    socketio.start_background_task(read_and_emit)
    socketio.run(app, host='0.0.0.0', port=5000)
