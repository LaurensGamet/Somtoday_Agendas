# webhook_listener.py
from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # You can check headers or payload here if needed
    subprocess.Popen(["/home/laurens/Somtoday_Agendas/.Reset.sh"])
    return "Script started", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
