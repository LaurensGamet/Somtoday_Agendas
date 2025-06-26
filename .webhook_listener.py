from flask import Flask, request, jsonify, Response
from flask_sock import Sock
import base64
import subprocess
import os
import pty
import select
import threading

app = Flask(__name__)
sock = Sock(app)

# -------------------------
# Basic HTTP endpoints
# -------------------------

@app.route('/api/reset', methods=['GET', 'POST'])
def reset_script():
    subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.Reset.sh"])
    return "Reset script started", 200

@app.route('/api/restart', methods=['GET', 'POST'])
def restart_script():
    subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.Restart.sh"])
    return "Restart script started", 200

@app.route('/api/updateagenda', methods=['GET', 'POST'])
def updateagenda_script():
    subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.run-updater.sh"])
    return "Update script started", 200

@app.route('/api/autostart', methods=['GET', 'POST'])
def autostart_script():
    subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.Autostart.sh"])
    return "Autostart script started", 200

@app.route('/api/reboot', methods=['GET', 'POST'])
def reboot_script():
    subprocess.Popen(["sudo", "reboot", "now"])
    return "Rebooting", 200

@app.route('/api/updaterepo', methods=['GET', 'POST'])
def updatelocalrepo_script():
    subprocess.Popen(["sudo", "bash", "/home/laurens/Somtoday_Agendas/.updatelocalrepo.sh"])
    return "Updating Local Repo", 200

# -------------------------
# Debug route (optional)
# -------------------------

@app.route('/api/debug')
def debug():
    # Only keep stringifiable environment keys and values
    safe_env = {}
    for k, v in request.environ.items():
        try:
            safe_env[k] = str(v)
        except Exception:
            safe_env[k] = "<unserializable>"
    return jsonify(safe_env)

@app.route("/api/whoami")
def whoami():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Basic "):
        return Response(
            "❌ Not authorized. Please reload and login.\r\n",
            status=401,
            headers={"WWW-Authenticate": 'Basic realm="Login Required"'}
        )

    encoded = auth_header.split(" ")[1]
    decoded = base64.b64decode(encoded).decode()
    username = decoded.split(":")[0]
    return jsonify({"username": username})

@sock.route('/api/terminal')
def terminal(ws):
    user = request.args.get("user")
    if not user:
        ws.send("❌ No user provided.\n")
        return

    import pwd
    try:
        user_info = pwd.getpwnam(user)
        user_home = user_info.pw_dir
        user_uid = user_info.pw_uid
        user_shell = user_info.pw_shell or "/bin/bash"
    except KeyError:
        ws.send(f"❌ User '{user}' not found on system.\n")
        return

    def read_pty(fd):
        while True:
            try:
                rlist, _, _ = select.select([fd], [], [], 0.1)
                if fd in rlist:
                    output = os.read(fd, 1024)
                    if output:
                        try:
                            ws.send(output.decode(errors='ignore'))
                        except:
                            break
                    else:
                        break
            except Exception:
                break

    def start_shell():
        pid, fd = pty.fork()
        if pid == 0:
            # Child process
            os.setuid(user_uid)
            os.chdir(user_home)
            os.environ["HOME"] = user_home
            os.environ["USER"] = user
            os.environ["LOGNAME"] = user
            os.environ["SHELL"] = user_shell
            os.environ["TERM"] = "xterm-256color"
            os.environ["PATH"] = os.environ.get("PATH", "/usr/bin:/bin")
            os.execvp(user_shell, [user_shell])
        else:
            # Parent process
            threading.Thread(target=read_pty, args=(fd,), daemon=True).start()

            while True:
                try:
                    data = ws.receive()
                    if data is None:
                        break
                    os.write(fd, data.encode())
                except:
                    break
            try:
                os.close(fd)
            except:
                pass

    start_shell()

def get_uid(username):
    import pwd
    return pwd.getpwnam(username).pw_uid

@app.route("/api/logout")
def logout():
    return Response(
        "Logged out",
        401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
