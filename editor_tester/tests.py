import json

from tornado import gen
from tornado.websocket import websocket_connect


@gen.coroutine
def test_mission_tests(url, mission_tests):
    for test in mission_tests:
        yield test_mission_test(url, test)


#out {"action":"get_initial","data":{"action":"get_initial","mission":"hamming_distance"}}	85
# {"action": "initial", "data": {"connectionId": "c5afff019c9149abb6451138dcf8a805", "code": "def hamming(n, m):\n return 0\n\nif __name__ == '__main__':\n # These \"asserts\" using only for self-checking and not necessary for auto-testing\n assert hamming(117, 17) == 3, \"First example\"\n assert hamming(1, 2) == 2, \"Second example\"\n assert hamming(16, 15) == 5, \"Third example\"\n", "description": "The Hamming distance between two binary integers is the number of bit positions that differs\n([read more about the Hamming distance on Wikipedia](http://en.wikipedia.org/wiki/Hamming_distance)).\nFor example:\n\n```\n117 = 0 1 1 1 0 1 0 1\n 17 = 0 0 0 1 0 0 0 1\n H = 0+1+1+0+0+1+0+0 = 3\n```\n\nYou are given two positive numbers (N, M) in decimal form.\nYou should calculate the Hamming distance between these two numbers in binary form.\n"}, "request_id": null}	886
#out {"action":"check","data":{"code":"def hamming(n, m):\n return 0\n\nif __name__ == '__main__':\n # These \"asserts\" using only for self-checking and not necessary for auto-testing\n assert hamming(117, 17) == 3, \"First example\"\n assert hamming(1, 2) == 2, \"Second example\"\n assert hamming(16, 15) == 5, \"Third example\"\n"}}	346
# {"action": "pre_test", "data": {"representation": "hamming(117, 17)"}, "request_id": null}	90
# {"action": "post_test", "data": {"actual_result": 0, "expected_result": 3, "test_passed": false, "additional_data": 3}, "request_id": null}	139
# {"action": "results", "data": {"action": "check", "additional_data": {"description": null}, "success": false}, "request_id": null}	130
# {"action": "ping", "data": null, "request_id": null}	52
#out {"action":"pong","data":{}}	27



@gen.coroutine
def test_mission_test(url, mission_test):

    ws_client = WebSocketClient(url)
    handler = MessageHandler(ws_client)

    yield ws_client.connect()
    while True:
        msg = yield ws_client.ws.read_message()
        if msg is None:
            break
        print(msg)
        yield handler.handle(msg)


class WebSocketClient(object):
    CONNECT_TIMEOUT = 10

    def __init__(self, url):
        self.url = url
        self.ws = None

    @gen.coroutine
    def connect(self):
        self.ws = yield websocket_connect(self.url, connect_timeout=self.CONNECT_TIMEOUT)

    @gen.coroutine
    def get_initial(self, mission_slug):
        # {"action":"get_initial","data":{"action":"get_initial","mission":"hamming_distance"}}
        yield self.send_message(action='get_initial', data={
            "action": "get_initial",
            "mission": mission_slug
        })

    @gen.coroutine
    def check(self, code):
        # {"action":"check","data":{"code":""}}	346
        yield self.send_message(action='check', data={
            "code": code
        })

    @gen.coroutine
    def pong(self):
        # {"action":"pong","data":{}}
        yield self.send_message(action='pong')

    @gen.coroutine
    def send_message(self, action, data=None):
        message = json.dumps({"action": action, "data": data})
        yield self.ws.write_message(message)


class MessageHandler(object):

    def __init__(self, ws_client):
        self._ws_client = ws_client
        self._handlers = {
            'ping': self.pong()
        }

    @gen.coroutine
    def handle(self, message):
        data = json.loads(message)
        action = data.get('action')
        if action is None:
            raise Exception("WTF msg: {}".format(message))

        yield self._handlers[action](data)

    @gen.coroutine
    def pong(self):
        self._ws_client.pong()