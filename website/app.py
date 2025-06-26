from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_sock import Sock
import os, json, pty, select, threading, pwd, subprocess

app = Flask(__name__)
app.secret_key = 'madeliefishot'  # Change this!
sock = Sock(app)

# Load credentials
with open(os.path.join(os.path.dirname(__file__), "credentials.json")) as f:
    credentials = json.load(f)

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')
        if user in credentials and credentials[user] == pw:
            session['username'] = user
            return redirect(url_for('index'))
        return render_template('login.html', error='❌ Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/whoami')
def whoami():
    if 'username' in session:
        return jsonify({'username': session['username']})
    return jsonify({'username': None}), 401

@sock.route('/api/terminal')
def terminal(ws):
    user = session.get('username')
    if not user:
        ws.send("❌ Not logged in.\n")
        return

    try:
        user_info = pwd.getpwnam(user)
    except KeyError:
        ws.send(f"❌ User '{user}' not found on system.\n")
        return

    user_home = user_info.pw_dir
    user_uid = user_info.pw_uid
    user_shell = user_info.pw_shell or "/bin/bash"

    def read_pty(fd):
        while True:
            try:
                rlist, _, _ = select.select([fd], [], [], 0.1)
                if fd in rlist:
                    output = os.read(fd, 1024)
                    if output:
                        ws.send(output.decode(errors='ignore'))
                    else:
                        break
            except:
                break

    pid, fd = pty.fork()
    if pid == 0:
        os.setuid(user_uid)
        os.chdir(user_home)
        os.environ.update({
            "HOME": user_home,
            "USER": user,
            "LOGNAME": user,
            "SHELL": user_shell,
            "TERM": "xterm-256color",
            "PATH": os.environ.get("PATH", "/usr/bin:/bin")
        })
        os.execvp(user_shell, [user_shell])
    else:
        threading.Thread(target=read_pty, args=(fd,), daemon=True).start()
        while True:
            try:
                data = ws.receive()
                if data is None:
                    break
                os.write(fd, data.encode())
            except:
                break
        os.close(fd)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
