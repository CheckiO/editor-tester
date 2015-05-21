

def get_missions():
    return ({
        'mission_slug': 'striped_words',
        'code': '''
from re import I, findall

VOWELS = "AEIOUY"
CONSONANTS = "BCDFGHJKLMNPQRSTVWXZ"


def striped_words(text):
    pattern = r'(?:\b(?:[{}][{}])+[{}]?\b)'
    regex = '({}|{})'.format(*[pattern] * 2).format(*[VOWELS, CONSONANTS] * 3)
    return len(findall(regex, text, I))
        ''',
        'success': True
    },)
