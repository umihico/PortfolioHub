html_dir = "../umihico.github.io/thumbnailed-portfolio-websites/"
import tinydb

que = tinydb.Query()


def load_db():
    content_tinydb = tinydb.TinyDB('content_tinydb.json')
    return content_tinydb


content_tinydb = load_db()


def load_location_db():
    location_db = tinydb.TinyDB('location.json')
    return location_db


location_db = load_location_db()


def chunks(list_, chunk_len):
    '''
    chunks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    >> [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    '''
    return list(list_[i:i + chunk_len] for i in range(0, len(list_), chunk_len))


def gen_filename(full_name):
    return 'gifs/' + full_name.replace('/', '-') + '.gif'


def raise_with_printed_args(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(func.__name__, args, kwargs)
            raise
    return wrapper


import re as _re


def numberize(string):
    return _re.sub(r'\D', '', string)


def numberize_int(string):
    return int(numberize(string))
