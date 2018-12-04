from scraping import url_to_gif
from api import iter_repo, get_userlocation_rawjson
import pprint
from no_thanks import no_thanks
from common import html_dir,  gen_filename, db
import os
from PIL import Image
import time
from geotag_modifier import geotag
import tqdm
from create_rawdb import rawdb

import datetime
import os


def del_if_too_old(repo):
    disappear_days = (time.time() - repo['db_updated_at']) // (60 * 60 * 24)
    if disappear_days > 7:
        print('del', disappear_days, 'days', repo['full_name'],)
        db.del_repo(repo)


def daily_update():
    for repo, raw_repo in zip_longest_db_rawdb():
        if repo is None:
            print('NEW!!', raw_repo['full_name'])
            update_repo(raw_repo)
        elif raw_repo is None:
            del_if_too_old(repo)
        else:
            if repo_is_updated(repo, raw_repo) or not git_exist(raw_repo):
                update_repo(raw_repo)


def git_exist(repo):
    filename = html_dir + gen_filename(repo['full_name'])
    return bool(os.path.exists(filename))


def repo_is_updated(repo, raw_repo):
    def time2day(raw_updated_at):
        # raw_updated_at = "2011-01-26T19:06:43Z"
        # updated_at = (2011,1,26)
        updated_at = tuple([int(s) for s in raw_updated_at[:10].split('-')])
        return updated_at

    def gif_date(repo):
        filename = html_dir + gen_filename(repo['full_name'])
        date = datetime.date.fromtimestamp(
            os.stat(filename).st_mtime) + datetime.timedelta(days=1)
        created_at = (date.year, date.month, date.day)
        return created_at

    # gif_date(repo))
    return bool(time2day(raw_repo['updated_at']) > time2day(repo['updated_at']))


def update_repo(repo):
    if not repo['homepage'] and repo['full_name'].endswith('.github.io'):
        reponame = repo['full_name'].split('/')[1]
        if repo['username'] == reponame.replace(".github.io", ''):
            repo['homepage'] = "https://" + reponame
    repo['homepage_exist'] = bool(repo['homepage'])
    if can_update_repo(repo):
        filename = html_dir + gen_filename(repo['full_name'])
        gif_success = url_to_gif(repo['homepage'], filename)
    else:
        gif_success = False
    repo['gif_success'] = gif_success
    repo['db_updated_at'] = time.time()
    db.upsert(repo)

#


def can_update_repo(repo):
    if not repo['homepage_exist']:
        return False


def zip_longest_db_rawdb():
    rawdb_dict = {raw_repos['full_name']: raw_repos for raw_repos in rawdb.all()}
    db_dict = {repos['full_name']: repos for repos in db.all()}
    full_names = list(set([*rawdb_dict.keys(), *db_dict.keys()]))
    for full_name in tqdm.tqdm(full_names):
        yield db_dict.get(full_name),  rawdb_dict.get(full_name)


if __name__ == '__main__':
    # optional_edit_content_tinydb()
    # update_location()
    # download_all()
    daily_update()
    # update_location()
