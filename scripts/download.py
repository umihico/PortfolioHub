from scraping import url_to_gif
from api import iter_repo, get_userlocation_rawjson
import pprint
from no_thanks import no_thanks
from common import html_dir,  gen_filename
from dbs import rawdb, db, ldb
import os
from PIL import Image
import time
from geotag_modifier import geotag
import tqdm
from star import star_repo
import datetime
import os

DELETE_IF_MISSING_THIS_TIMES = 10


def del_if_too_old(repo):
    missing_times = repo.get('missing_times', 0)
    missing_times += 1
    if missing_times == DELETE_IF_MISSING_THIS_TIMES:
        print('del', disappear_days, 'days', repo['full_name'],)
        del db[db.gen_key(repo)]
    else:
        repo['missing_times'] = missing_times


def update_last_found_date(repo):
    repo['last_found_date'] = int(time.time())
    db.upsert(repo)


def daily_update():
    for repo, raw_repo in zip_longest_db_rawdb():
        if raw_repo and repo:
            update_last_found_date(repo)
        if raw_repo and raw_repo['stargazers_count'] == 0:
            star_repo(raw_repo['full_name'])
        if repo is None:
            print('NEW!!', raw_repo['full_name'])
            update_repo(raw_repo)
        elif raw_repo is None:
            del_if_too_old(repo)
        else:
            if repo_is_updated(repo, raw_repo) or not git_exist(raw_repo):
                update_repo(raw_repo)
            else:

                repo['reponame'] = raw_repo['reponame']
                repo['api_url'] = raw_repo['api_url']
                db.upsert(repo)
    db.save()


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
    update_last_found_date(repo)
    db.upsert(repo)

#


def can_update_repo(repo):
    if not repo['homepage_exist']:
        return False
    return True


def zip_longest_db_rawdb():
    rawdb_dict = {raw_repos['html_url']: raw_repos for raw_repos in rawdb.all()}
    db_dict = {repos['html_url']: repos for repos in db.all()}
    html_urls = list(set([*rawdb_dict.keys(), *db_dict.keys()]))
    new_urls = set(html_urls) - set(db_dict.keys())
    old_urls = set(html_urls) - set(rawdb_dict.keys())
    will_deleting_cnt = len([t for t in [db.get({'html_url': html_url}).get('missing_times', 0)
                                         for html_url in old_urls] if t >= DELETE_IF_MISSING_THIS_TIMES - 1])
    print("NEW", len(new_urls), 'OLD', will_deleting_cnt)
    for html_url in tqdm.tqdm(html_urls):
        yield db_dict.get(html_url),  rawdb_dict.get(html_url)


if __name__ == '__main__':
    # optional_edit_content_tinydb()
    # update_location()
    # download_all()
    daily_update()
    # update_location()
