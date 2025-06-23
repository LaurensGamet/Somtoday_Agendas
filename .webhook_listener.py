from flask import Flask, request
from flask_socketio import SocketIO, emit
import os, pty, select, subprocess

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # allow connections from 8080

# Your original redirect endpoints
@app.route('/reset', methods=['GET', 'POST'])
def reset_script():
    subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.Reset.sh"])
    return "Reset script started", 200

@app.route('/restart', methods=['GET', 'POST'])
def restart_script():
    subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.Restart.sh"])
    return "Restart script started", 200

@app.route('/update', methods=['GET', 'POST'])
def update_script():
    subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.run-updater.sh"])
    return "Update script started", 200

@app.route('/autostart', methods=['GET', 'POST'])
def autostart_script():
    subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.Autostart.sh"])
    return "Autostart script started", 200

@app.route('/reboot', methods=['GET', 'POST'])
def reboot_script():
    subprocess.Popen(["sudo", "reboot", "now"])
    return "Rebooting", 200

# === Terminal WebSocket logic ===
VALID_USERNAME = "pi"
VALID_PASSWORD = "raspberry"
sessions = {}

@socketio.on("connect")
def handle_connect():
    sid = request.sid
    sessions[sid] = {"stage": "login", "username": "", "fd": None, "pid": None}
    emit("pty_output", "raspberry login: ")

@socketio.on("pty_input")
def handle_input(data):
    sid = request.sid
    session = sessions[sid]

    if session["stage"] == "login":
        session["username"] = data.strip()
        session["stage"] = "password"
        emit("pty_output", "\r\nPassword: ")
    elif session["stage"] == "password":
        if session["username"] == VALID_USERNAME and data.strip() == VALID_PASSWORD:
            session["stage"] = "authenticated"
            pid, fd = pty.fork()
            if pid == 0:
                subprocess.run(["/bin/bash"])
            else:
                session["fd"] = fd
                session["pid"] = pid
                emit("pty_output", "\r\nWelcome to Raspberry Pi!\r\n\n")
        else:
            session["stage"] = "login"
            emit("pty_output", "\r\nLogin incorrect\r\n\nraspberry login: ")
    elif session["stage"] == "authenticated":
        os.write(session["fd"], data.encode())

@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    if sid in sessions:
        if sessions[sid].get("fd"):
            os.close(sessions[sid]["fd"])
        del sessions[sid]

def stream_pty_output():
    while True:
        for sid, session in sessions.items():
            if session["stage"] == "authenticated" and session["fd"]:
                if select.select([session["fd"]], [], [], 0)[0]:
                    output = os.read(session["fd"], 1024).decode(errors="ignore")
                    socketio.emit("pty_output", output, room=sid)

if __name__ == '__main__':
    socketio.start_background_task(stream_pty_output)
    socketio.run(app, host='0.0.0.0', port=5000)
