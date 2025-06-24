from flask import Flask, request
import subprocess

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
