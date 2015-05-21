from tornado.ioloop import IOLoop

from parser import get_missions
from tests import test_mission_tests


# ws://www.empireofcode.com/ws/main/?EIO=3&transport=websocket
if __name__ == "__main__":
    url = 'ws://www.empireofcode.com/ws/editor/'  # TODO: move to arg

    io_loop = IOLoop.instance()

    missions = get_missions()
    for mission_tests in missions:
        test_mission_tests(url, mission_tests)

    io_loop.start()
