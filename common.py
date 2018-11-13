html_dir = "../umihico.github.io/thumbnailed-portfolio-websites/"
from tinydb import TinyDB


def load_db():
    content_tinydb = TinyDB('content_tinydb.json')
    return content_tinydb


def chunks(list_, chunk_len):
    '''
    chunks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    >> [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    '''
    return list(list_[i:i + chunk_len] for i in range(0, len(list_), chunk_len))


def gen_filename(full_name):
    return 'gifs/' + full_name.replace('/', '-') + '.gif'


import re as _re


def numberize(string):
    return _re.sub(r'\D', '', string)


def numberize_int(string):
    return int(numberize(string))
