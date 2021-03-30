from django.conf import settings
from slacker import Slacker
import json

def slack_notify(text=None, channel='#test', username="책화점_알리미",attachments=None):
    config_secret = json.loads(open(settings.CONFIG_SECRET_FILE).read())
    token = config_secret['SLACK_NOTIFY']['TOKEN']
    slack = Slacker(token)
    slack.chat.post_message(
        text=text,
        channel=channel,
        username=username,
        attachments=attachments)