import slack
import os
from pathlib import Path
from dotenv import load_dotenv
import ssl
from flask import Flask
from slackeventsapi import SlackEventAdapter
 
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)

client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'], ssl=ssl_context)

MY_USER_ID = client.api_call("auth.test")['user_id']
RESPONDED = False
app_id = 'U0546RVE66Q'

@slack_event_adapter.on('message')
def handle_message(event_data):

    global RESPONDED
    global app_id
    message = event_data['event']
    channel_id = message['channel']
    user_id = message['user']
    text = message.get('text')

    if app_id != user_id and not RESPONDED:
        client = slack.WebClient(token=os.environ['SLACK_USER_TOKEN'], ssl=ssl_context)
        client.chat_postMessage(channel=channel_id, text=f'<@{app_id}> {text}')
        RESPONDED = True
    elif MY_USER_ID != user_id and app_id != user_id and RESPONDED:
        RESPONDED = False


if __name__ == "__main__":
    app.run(debug=True)