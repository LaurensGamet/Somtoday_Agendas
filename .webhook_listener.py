# webhook_listener.py
from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/reset', methods=['GET', 'POST'])
def webhook():
    # You can check headers or payload here if needed
    subprocess.Popen(["/home/laurens/Somtoday_Agendas/.Reset.sh"])
    return "Script started", 200

@app.route('/restart', methods=['GET', 'POST'])
def webhook():
    # You can check headers or payload here if needed
    subprocess.Popen(["/home/laurens/Somtoday_Agendas/.Restart.sh"])
    return "Script started", 200

@app.route('/update', methods=['GET', 'POST'])
def webhook():
    # You can check headers or payload here if needed
    subprocess.Popen(["/home/laurens/Somtoday_Agendas/.run-updater.sh"])
    return "Script started", 200

@app.route('/autostart', methods=['GET', 'POST'])
def webhook():
    # You can check headers or payload here if needed
    subprocess.Popen(["/home/laurens/Somtoday_Agendas/.Autostart.sh"])
    return "Script started", 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
