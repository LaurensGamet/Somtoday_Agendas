from flask import Flask, request
import subprocess
import shlex

app = Flask(__name__)

@app.route('/reset', methods=['GET', 'POST'])
def reset_script():
    subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.Reset.sh"])
    return "Reset script started", 200

@app.route('/restart', methods=['GET', 'POST'])
def restart_script():
    subprocess.Popen(["sudo", "/home/laurens/Somtoday_Agendas/.Restart.sh"])
    return "Restart script started", 200

@app.route('/updateagenda', methods=['GET', 'POST'])
def updateagenda_script():
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

@app.route('/updaterepo', methods=['GET', 'POST'])
def updatelocalrepo_script():
    subprocess.Popen(["sudo", "bash", "/home/laurens/Somtoday_Agendas/.updatelocalrepo.sh"])
    return "Updating Local Repo", 200

@app.route('/terminal', methods=['POST'])
def terminal():
    cmd = request.form.get('command')
    if not cmd:
        return "No command provided", 400
    try:
        command_list = shlex.split(cmd)
        result = subprocess.check_output(command_list, stderr=subprocess.STDOUT, text=True)
        return result, 200
    except subprocess.CalledProcessError as e:
        return e.output, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
