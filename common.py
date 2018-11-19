html_dir = "../umihico.github.io/thumbnailed-portfolio-websites/"
import tinydb
import time

que = tinydb.Query()


def load_db():
    content_tinydb = tinydb.TinyDB('content_tinydb.json')
    return content_tinydb


content_tinydb = load_db()


def load_location_db():
    location_db = tinydb.TinyDB('location.json')
    return location_db


location_db = load_location_db()


class DictTinyDB():
    def __init__(self, filename, unique_key):
        self.db = tinydb.TinyDB(filename)
        self.unique_key = unique_key
        self.que = getattr(tinydb.Query(), self.unique_key)

    def all(self):
        for d in self.db.all():
            yield d

    def upsert(self, dict_data):
        unique_value = dict_data[self.unique_key]
        old_data = self.get(unique_value, else_value=dict())
        new_data = {**old_data}
        new_data.update(dict_data)
        self.db.upsert(new_data, self.que == unique_value)

    def get_repo(self, repo, else_value=None):
        unique_value = repo[self.unique_key]
        return self.get(unique_value, else_value=else_value)

    def get(self, unique_value, else_value=None):
        rows = self.db.search(self.que == unique_value)
        return rows[0] if rows else else_value

    def del_repo(self, repo):
        self.db.remove(self.que == repo[self.unique_key])


db = DictTinyDB('db.json', 'html_url')


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


def get_username(full_name):
    return full_name.split('/')[0]


def update_db(repo):
    dict_data = _reduce_amount(repo)
    dict_data['db_updated_at'] = time.time()
    db.upsert(dict_data)


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


if __name__ == '__main__':
    import tqdm
    # for d in tqdm.tqdm(content_tinydb.all()):
    #     db.upsert(d)

    user_dicts = {d['username']: d for d in location_db.all()}
    for d in tqdm.tqdm(db.all()):
        username = get_username(d['full_name'])
        # print(username)
        location_dict = user_dicts.get(username)
        if location_dict:
            # print(username)
            d['userdict'] = location_dict
            update_db(d)
