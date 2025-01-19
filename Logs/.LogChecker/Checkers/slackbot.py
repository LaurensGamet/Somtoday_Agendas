from slack_bolt import App
from slackcredentials import App_Token

# Initialize the Slack app
app = App(token=App_Token)

# Simple command response
@app.command("/hello")
def handle_hello_command(ack, respond):
    ack()  # Acknowledge the command
    respond("Hello! I'm running on a Raspberry Pi.")

# Event listener for messages
@app.event("message")
def handle_message_events(body, say):
    user = body['event']['user']
    text = body['event']['text']
    say(f"Hi <@{user}>, you said: {text}")

# Start the app
if __name__ == "__main__":
    app.start(port=3000)
