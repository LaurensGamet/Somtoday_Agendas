from flask import Flask, request, jsonify
from flask_sock import Sock
import subprocess
import os
import pty
import select
import threading

app = Flask(__name__)
sock = Sock(app)

# === ROUTES FOR BUTTONS ===

@app.route('/api/reset', methods=['GET'])
def reset():
    subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.Reset.sh"])
    return "Reset script started", 200

@app.route('/api/restart', methods=['GET'])
def restart():
    subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.Restart.sh"])
    return "Restart script started", 200

@app.route('/api/updateagenda', methods=['GET'])
def update_agenda():
    subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.run-updater.sh"])
    return "Update Agenda script started", 200

@app.route('/api/autostart', methods=['GET'])
def autostart():
    subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.Autostart.sh"])
    return "Autostart script started", 200

@app.route('/api/reboot', methods=['GET'])
def reboot():
    subprocess.Popen(["sudo", "reboot"])
    return "Rebooting system...", 200

@app.route('/api/updaterepo', methods=['GET'])
def update_repo():
    subprocess.Popen(["sudo", "bash", "/home/laurens/Somtoday_Agendas/.updatelocalrepo.sh"])
    return "Updating local repo...", 200

# === RETURN USERNAME TO FRONTEND ===

@app.route('/api/whoami', methods=['GET'])
def whoami():
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Basic '):
        return 'Not authorized', 401

    import base64
    try:
        encoded = auth.split(' ')[1]
        decoded = base64.b64decode(encoded).decode('utf-8')
        username = decoded.split(':')[0]
        return jsonify({'username': username})
    except Exception:
        return 'Invalid auth', 400

# === TERMINAL OVER WEBSOCKET ===

@sock.route('/api/terminal')
def terminal(ws):
    username = request.args.get('user')
    if not username:
        ws.send("❌ No user provided")
        ws.close()
        return

    try:
        uid = subprocess.check_output(['id', '-u', username]).decode().strip()
        gid = subprocess.check_output(['id', '-g', username]).decode().strip()
    except subprocess.CalledProcessError:
        ws.send(f"❌ User '{username}' not found")
        ws.close()
        return

    pid, fd = pty.fork()
    if pid == 0:
        os.setgid(int(gid))
        os.setuid(int(uid))
        os.execv('/bin/bash', ['/bin/bash'])

    def read_from_pty():
        while True:
            try:
                data = os.read(fd, 1024)
                if not data:
                    break
                ws.send(data.decode(errors='ignore'))
            except Exception:
                break

    thread = threading.Thread(target=read_from_pty)
    thread.daemon = True
    thread.start()

    while True:
        try:
            data = ws.receive()
            if data is None:
                break
            os.write(fd, data.encode())
        except Exception:
            break

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
