import sys
import json
import traceback

from utils import send_request
from utils import parser

class App:
    def __init__(self, url, pool):
        self.url     = url
        self.pool    = pool

    def connect(self):
        try:
            response_in_html = send_request(self.url)

            if not response_in_html:
                return None

            return parser(response_in_html, self.pool)

        except:
            traceback.print_exc()
            return None

    def run(self):
        """

        Starting point of the class APP

        """
        try:
            return self.connect()
        except:
            return False
