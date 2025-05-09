import os 
from flask import abort, make_response
import requests

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_API_URL = "https://slack.com/api/chat.postMessage"

def send_slack_notification(message, channel="#task-notifications"):
    headers = {
        "Authorization": SLACK_BOT_TOKEN,
        "Content-Type": "application/json"
    }

    request_body = {
        "channel": channel,
        "text": message
    }

    try:
        response = requests.post(SLACK_API_URL, headers=headers, json=request_body)

    except: # for any exception
        abort(make_response({"message": f"Slack API error"}, 400))


