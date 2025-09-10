import time
import json
import requests
from slackcredentials import Incoming_Webhook_URL

log_file_path = '/home/laurens/Somtoday_Agendas/Logs/Loukas.log'
keywords = ["error", "failed", "exception", "fatal"]  # Keywords to detect

slack_webhook = Incoming_Webhook_URL
slack_message_template = {
        "username": "Somtoday Loukas",
        "text": "Warning!\nThe latest log contained an error!\n<https://github.com/LaurensGamet/Somtoday_Agendas/blob/main/Logs|Click here to view logs>",
#    	"icon_url": "http://141.224.230.177:8080/.Checkers/laurens.jpg"
}

def check_for_errors():
    with open(log_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if any(keyword.lower() in line.lower() for keyword in keywords):
                return True
    return False

def trigger_action():
    # Prepare the Slack message
    slack_message = json.dumps(slack_message_template)
    response = requests.post(
        slack_webhook,
        data=slack_message,
        headers={'Content-Type': 'application/json'}
    )
    print ("Message Sent!")
    if response.status_code != 200:
        raise ValueError(
            'Request to Slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

# Continuously monitor the log file every 30 seconds
while True:
    if check_for_errors():
        trigger_action()  # Trigger action if error is found
        # Wait for 60 minutes before checking again
        time.sleep(60 * 60)
    else:
        # If no error is found, check again after a shorter interval
        time.sleep(30)
