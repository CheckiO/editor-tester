import argparse
import logging

import coloredlogs

from tests import Toster

coloredlogs.install(show_name=False)
logger = logging.getLogger(__file__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Command line mission tester')
    parser.add_argument('-d', dest='domain', default='www.empireofcode.com',
                        help='Example: www.empireofcode.com', required=True)
    parser.add_argument('-s', dest='session_id', help='User session id from cookie', required=True)
    parser.add_argument('-b', dest='basic', help='Basic auth key')
    options = parser.parse_args()

    toster = Toster(options.domain, options.session_id, options.basic)
    toster.run_tests()
