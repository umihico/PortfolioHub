html_dir = "../gh-pages/"

import time


def chunks(list_, chunk_len):
    '''
    chunks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    >> [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    '''
    return list(list_[i: i + chunk_len] for i in range(0, len(list_), chunk_len))


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


def _reduce_amount(repo):
    keys = ["html_url", 'description', "size", 'stargazers_count', 'homepage',
            'watchers_count', 'forks', 'watchers', 'score', 'full_name', 'created_at', 'updated_at', 'gif_success', 'homepage_exist', 'userdict']
    return {k: v for k, v in repo.items() if k in keys}


import codecs as _codecs
import ast as _ast
from pprint import pformat as _pformat


def save_as_txt(filename, data, mode='w'):
    with _codecs.open(filename, mode, 'utf-8') as f:
        f.write(_pformat(data))


def load_from_txt(filename):
    with _codecs.open(filename, 'r', 'utf-8') as f:
        return _ast.literal_eval(f.read())


import hashlib


def hash_username(username):
    sha256 = hashlib.sha256()
    sha256.update(username.lower().encode())
    hashed_text = sha256.hexdigest()
    return hashed_text


def test_hash_username(username='umihico'):
    print(hash_username(username))


if __name__ == '__main__':
    test_hash_username(username='umihico')
