# messed up
from api import _json_iter
import hashlib
from itertools import zip_longest
from no_thanks import no_thanks
from dbs import rawdb, db, ldb


def create_rawdb(topic="portfolio-website"):
    rawdb.erase_all()
    for json in _json_iter(topic=topic):
        total_count, repos = json['total_count'], json['items']
        for repo in repos:
            repo['username'], repo['reponame'] = repo['full_name'].split('/')
            repo['api_url'] = json['url']
            if should_skip(repo['username']):
                continue
            repo = _reduce_amount(repo)
            rawdb.upsert(repo)
    rawdb.save()


def _reduce_amount(repo):
    keys = ['last_found_date', "html_url",  'api_url', 'stargazers_count', 'homepage',
            'forks', 'full_name',  'updated_at', 'gif_success', 'homepage_exist', 'userdict', 'requests_success', 'pushed_at', 'username', 'reponame']
    return {k: v for k, v in repo.items() if k in keys}


def should_skip(username):
    skip_bool = hash_username(username) in no_thanks
    if skip_bool:
        print('skipped', username)
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
