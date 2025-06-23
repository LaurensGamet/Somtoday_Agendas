from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO, emit
import os, pty, select, subprocess

app = Flask(__name__, static_url_path="", static_folder=".")
socketio = SocketIO(app)

VALID_USERNAME = "pi"
VALID_PASSWORD = "raspberry"
sessions = {}

@app.route("/")
def home():
    return send_from_directory(".", "redirect_center.html")

@app.route("/reset")
def reset():
    subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.Reset.sh"])
    return "Reset started", 200

@app.route("/restart")
def restart():
    subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.Restart.sh"])
    return "Restart started", 200

@app.route("/update")
def update():
    subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.run-updater.sh"])
    return "Update started", 200

@app.route("/autostart")
def autostart():
    subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.Autostart.sh"])
    return "Autostart started", 200

@app.route("/reboot")
def reboot():
    subprocess.Popen(["sudo", "reboot", "now"])
    return "Rebooting", 200

@socketio.on("connect")
def on_connect():
    sid = request.sid
    sessions[sid] = {
        "stage": "login",
        "username": "",
        "fd": None,
        "pid": None
    }
    emit("pty_output", "raspberry login: ")

@socketio.on("pty_input")
def on_input(data):
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
def on_disconnect():
    sid = request.sid
    session = sessions.get(sid)
    if session:
        if session["fd"]:
            os.close(session["fd"])
        del sessions[sid]

def stream_output():
    while True:
        for sid, sess in sessions.items():
            if sess["stage"] == "authenticated" and sess["fd"]:
                if select.select([sess["fd"]], [], [], 0)[0]:
                    output = os.read(sess["fd"], 1024).decode(errors="ignore")
                    socketio.emit("pty_output", output, room=sid)

if __name__ == "__main__":
    socketio.start_background_task(stream_output)
    socketio.run(app, host="0.0.0.0", port=5000)
