import requests

import settings


def send_message_via_slack(channel, message):
	_response = requests.post(settings.SLACK_URL % channel, message.encode('UTF-8'))
	return 
