import logging
from pushover import Client


class PushoverHandler(logging.Handler):

    def __init__(self, api_token, user_key, title=None):
        logging.Handler.__init__(self)
        self.api_token = api_token
        self.user_key = user_key
        self.title = title


    def emit(self, record):
        client = Client(self.user_key, api_token=self.api_token)
        client.send_message(self.format(record), title=self.title)
