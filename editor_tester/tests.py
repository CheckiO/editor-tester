"""
out {"action":"get_initial","data":{"action":"get_initial","mission":"hamming_distance"}}	85
{"action": "initial", "data": {"connectionId": "c5afff019c9149abb6451138dcf8a805", "code": "def hamming(n, m):\n return 0\n\nif __name__ == '__main__':\n # These \"asserts\" using only for self-checking and not necessary for auto-testing\n assert hamming(117, 17) == 3, \"First example\"\n assert hamming(1, 2) == 2, \"Second example\"\n assert hamming(16, 15) == 5, \"Third example\"\n", "description": "The Hamming distance between two binary integers is the number of bit positions that differs\n([read more about the Hamming distance on Wikipedia](http://en.wikipedia.org/wiki/Hamming_distance)).\nFor example:\n\n```\n117 = 0 1 1 1 0 1 0 1\n 17 = 0 0 0 1 0 0 0 1\n H = 0+1+1+0+0+1+0+0 = 3\n```\n\nYou are given two positive numbers (N, M) in decimal form.\nYou should calculate the Hamming distance between these two numbers in binary form.\n"}, "request_id": null}	886
out {"action":"check","data":{"code":"def hamming(n, m):\n return 0\n\nif __name__ == '__main__':\n # These \"asserts\" using only for self-checking and not necessary for auto-testing\n assert hamming(117, 17) == 3, \"First example\"\n assert hamming(1, 2) == 2, \"Second example\"\n assert hamming(16, 15) == 5, \"Third example\"\n"}}	346
{"action": "pre_test", "data": {"representation": "hamming(117, 17)"}, "request_id": null}	90
{"action": "post_test", "data": {"actual_result": 0, "expected_result": 3, "test_passed": false, "additional_data": 3}, "request_id": null}	139
{"action": "results", "data": {"action": "check", "additional_data": {"description": null}, "success": false}, "request_id": null}	130
{"action": "ping", "data": null, "request_id": null}	52
out {"action":"pong","data":{}}	27

"""
import json
import logging
import time

import websocket

import settings
from parsers import get_missions

logger = logging.getLogger(__file__)


class Toster(object):

    def __init__(self, domain, session_id, basic=None):
        self.url = settings.MAIN_URLS.get(domain)
        if self.url is None:
            self.url = settings.CUSTOM_URL_TEMPLATE.format(domain)
        self.session_id = session_id
        self.basic_key = basic

    def run_tests(self):
        logger.info("Run tests")
        missions = get_missions()
        for mission_key, mission_tests in missions.items():
            self.test_mission_tests(mission_tests)

    def test_mission_tests(self, mission_tests):
        for test in mission_tests:
            logger.info("Start test item {}".format(test['name']))
            item_toster = ItemToster(self.url, self.session_id, self.basic_key, test)
            try:
                item_toster.test()
            except TestError as e:
                logger.error("Test {} has error: {}".format(test['name'], e))
            time.sleep(settings.DELAY_BETWEEN_TESTS)


class ItemToster(object):

    def __init__(self, url, session_id, basic_key, mission_test):
        self.ws_client = WebSocketClient(url, session_id, basic_key)
        self.mission_test = mission_test

    def test(self):
        self.ws_client.connect()
        self.test_initial_data()
        self.test_check()
        self.ws_client.close()

    def test_initial_data(self):
        self.ws_client.send_get_initial(self.mission_test['mission_slug'])
        initial_data = self.ws_client.read_message()
        # TODO: test

    def test_check(self):
        self.ws_client.send_check(self.mission_test['code'])
        message = self.ws_client.read_message()
        while message['action'] != 'results':
            message = self.ws_client.read_message()
        if message['data']['success'] != self.mission_test['success']:
            logger.error("Check not passed {}".format(self.mission_test['name']))
        else:
            logger.info(green("Check passed {}".format(self.mission_test['name'])))


class WebSocketClient(object):

    COOKIE = 'sessionid={}'
    # AUTH = 'Basic ZW1waXJlOlkwdVNoYWxsTm90UGFzczQy'
    AUTH_HEADER = 'Authorization: Basic {}'

    def __init__(self, url, session_id, basic_key):
        self.url = url
        self.session_id = session_id
        self.basic_key = basic_key
        self.ws = websocket.WebSocket()

    def connect(self):
        logger.info(self.url)
        header = []
        if self.basic_key:
            header.append(self.AUTH_HEADER.format(self.basic_key))

        self.ws.connect(self.url, header=header, cookie=self.COOKIE.format(self.session_id))

    def read_message(self):
        message = self.ws.recv()
        # logger.info("Handle {}".format(message))

        data = json.loads(message)
        action = data.get('action')
        if action == 'error':
            raise TestError(data['data'])
        if action == 'ping':
            self.pong(data.get('data'))
            return self.read_message()
        return data

    def send_get_initial(self, mission_slug):
        # {"action":"get_initial","data":{"action":"get_initial","mission":"hamming_distance"}}
        self.send_message(action='get_initial', data={
            "action": "get_initial",
            "mission": mission_slug
        })

    def send_check(self, code):
        # {"action":"check","data":{"code":""}}	346
        self.send_message(action='check', data={
            "code": code
        })

    def pong(self, data):
        # {"action":"pong","data":{}}
        self.send_message(action='pong', data=data)

    def send_message(self, action, data=None):
        message = json.dumps({"action": action, "data": data})
        # logger.info("Send message {} {}".format(type(message), message))
        self.ws.send(message)

    def close(self):
        self.ws.close()


class TestError(Exception):
    pass


def _wrap_with(code):

    def inner(text, bold=False):
        c = code
        if bold:
            c = "1;%s" % c
        return "\033[%sm%s\033[0m" % (c, text)
    return inner

red = _wrap_with('31')
green = _wrap_with('32')
