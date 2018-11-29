# messed up
from api import _json_iter
from common import DictTinyDB, db
import hashlib
from itertools import zip_longest
from no_thanks import no_thanks
rawdb = DictTinyDB(
    '../umihico.github.io/thumbnailed-portfolio-websites/rawdb.json', 'html_url')


def create_rawdb(topic="portfolio-website"):
    rawdb.db.purge()
    for json in _json_iter(topic=topic):
        total_count, repos = json['total_count'], json['items']
        for repo in repos:
            if should_skip(repo['full_name']):
                continue
            repo = _reduce_amount(repo)
            rawdb.upsert(repo)


def _reduce_amount(repo):
    keys = ["html_url",  'stargazers_count', 'homepage',
            'forks', 'full_name',  'updated_at', 'gif_success', 'homepage_exist', 'userdict', 'requests_success', 'pushed_at']
    return {k: v for k, v in repo.items() if k in keys}


def should_skip(full_name):
    username = full_name.split('/')[0]
    skip_bool = hash_username(username) in no_thanks
    if skip_bool:
        print('skipped', full_name)
    return skip_bool


def hash_username(username):
    sha256 = hashlib.sha256()
    sha256.update(username.lower().encode())
    hashed_text = sha256.hexdigest()
    return hashed_text


def test_hash_username(username='umihico'):
    print(hash_username(username))


if __name__ == '__main__':
    create_rawdb()
    # for d, rawd in zip_longest_db_rawdb():
    #     print(type(d), type(rawd))
