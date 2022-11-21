import requests
from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)
from requests.exceptions import ConnectionError, HTTPError

url = 'https://api.expo.dev/v2/push/send'

def send_notification( notifications ):
    response = PushClient().publish_multiple([PushMessage(**notification) for notification in notifications])
    print(response)
