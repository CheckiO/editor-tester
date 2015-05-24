import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DATA_DIR = os.path.join(BASE_DIR, 'tests_data')


def get_missions():
    missions = {}
    for file in os.listdir(TESTS_DATA_DIR):
        file_path = os.path.join(TESTS_DATA_DIR, file)
        if not os.path.isfile(file_path) or file.startswith('_'):
            continue
        key = file.split('.')
        if len(key) > 1:
            key = '.'.join(key[:-1])

        test_content = get_file_content(file_path)
        missions[key] = get_content_tests(test_content)

    return missions


def get_file_content(file_path):
    with open(file_path) as fp:
        return fp.read()


def get_content_tests(content):
    context = dict()
    exec(content, context)
    return context['TESTS']
