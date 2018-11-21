from scraping import url_to_gif
from api import iter_repo, get_userlocation_rawjson
import pprint
from no_thanks import no_thanks
from common import html_dir,  gen_filename, que, db, update_db, _reduce_amount, get_username, load_from_txt, save_as_txt, hash_username
import os
from PIL import Image
import time
from geotag_modifier import geotag
import tqdm


def optional_scraping_forcer(repo):
    return False
    # filename = html_dir + gen_filename(repo['full_name'])
    # im = Image.open(filename)
    # if max(im.size) < 500:
    #     print(im.size)
    #     return True
    # else:
    #     return False


def should_gif_download(repo):
    full_name = repo['full_name']
    if not repo['homepage_exist']:
        # print("no homepage", full_name)
        return False
    db_repo = db.get_repo(repo)
    if not db_repo:
        # print("found new", full_name)
        todays_new = load_from_txt('todays_new.txt')
        todays_new.append(full_name)
        save_as_txt('todays_new.txt', todays_new)
        return True
    filename = html_dir + gen_filename(repo['full_name'])
    if not os.path.exists(filename):
        # print("no gif yet", full_name)
        return True
    if _conv_updated_at_comparable(repo['updated_at']) > _conv_updated_at_comparable(db_repo['updated_at']) and time.time() - db_repo.get('db_updated_at', 0) > 60 * 60 * 24:

        # print("github updated", full_name)
        return True
    if optional_scraping_forcer(repo):
        # print("optional_scraping_forcer", full_name)
        return True
    # print("already done", full_name)
    return False


def _conv_updated_at_comparable(raw_updated_at):
    # raw_updated_at = "2011-01-26T19:06:43Z"
    # updated_at = (2011,1,26)
    updated_at = tuple([int(s) for s in raw_updated_at[:10].split('-')])
    return updated_at


def download_all():
    save_as_txt('todays_new.txt', [])
    chrome = None
    starttime = time.time()
    del_old_repo(starttime)
    for repo in iter_repo():
        if should_gif_download(repo):
            portfolio_url = repo['homepage']
            filename = html_dir + gen_filename(repo['full_name'])
            chrome, gif_success = url_to_gif(
                portfolio_url, filename, chrome)
            repo['gif_success'] = gif_success
        update_db(repo)
    update_location()
    del_no_thanks()
    todays_new = load_from_txt('todays_new.txt')
    print(todays_new)


def del_no_thanks_users():
    for d in db.all():
        if hash_username(d['username']) in no_thanks:
            db.remove(d)


def del_old_repo(starttime):
    for repo in db.all():
        disappear_days = (starttime - repo['db_updated_at']) // (60 * 60 * 24)
        if disappear_days > 7:
            print('del', disappear_days, 'days', repo['full_name'],)
            db.del_repo(repo)


def update_location():
    all_ = [d for d in db.all() if d['homepage_exist'] and d['gif_success']]
    limit_exceeded = False
    for d in tqdm.tqdm(sorted(all_, key=lambda d: (
            d['gif_success'] * -1, d.get('userdict', {}).get("updated_at", 0)))):
        if not limit_exceeded:
            username = get_username(d['full_name'])
            try:
                json = get_userlocation_rawjson(username)
                location = json['location']
            except Exception as e:
                limit_exceeded = True
                print(json)
                print(e)
                break
            else:
                d['userdict'] = {'username': username, 'location': location, 'tags': geotag(location),
                                 'updated_at': int(time.time())}
                update_db(d)
                time.sleep(1)


def optional_edit_content_tinydb():
    # url = 'derekargueta/Personal-Site'
    # content_tinydb.remove(que.full_name == url)
    # hit_repos = raw_api_repos.search(que.full_name == full_name)
    # print(hit_repos[0]['full_name'])
    # print(hit_repos[0]['html_url'])
    all_repo = content_tinydb.all()
    for repo in all_repo:
        if 'homepage' not in repo:
            print(repo['html_url'])
            content_tinydb.remove(que.html_url == repo['html_url'])


if __name__ == '__main__':
    # optional_edit_content_tinydb()
    # update_location()
    download_all()
    # update_location()
