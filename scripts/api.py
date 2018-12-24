
import requests
import pprint
import time
import datetime
import tinydb
from common import hash_username
from no_thanks import no_thanks


def _created_range_iter():
    month_list = [
        (1, 4, 0),
        (4, 7, 0),
        (7, 10, 0),
        (10, 1, 1),
    ]
    for year in range(2014, 9999):
        for start_month, end_month, yaer_adj in month_list:
            if datetime.date(year, start_month, 1) > datetime.date.today():
                raise StopIteration
            created_range = f"created:{year}-{str(start_month).zfill(2)}-01..{year + yaer_adj}-{str(end_month).zfill(2)}-01"
            yield created_range


def _test_created_range_iter():
    for created_range in _created_range_iter():
        print(created_range)


def github_api_get(url):
    headers = {
        'Accept': 'application/vnd.github.mercy-preview+json', }
    sleep_time = 10
    while True:
        response = requests.get(url, headers=headers)
        json = response.json()
        if 'message' in json and "API rate limit exceeded for " in json['message']:
            print("API rate limit exceeded")
            sleep_time *= 2
            print("sleeping", sleep_time)
            time.sleep(sleep_time)
        else:
            return response


def _json_iter(topic="portfolio-website"):
    last_GET_time = 0
    for created_range in _created_range_iter():
        for i in range(1, 9999):
            url = f'https://api.github.com/search/repositories?q=topic:{topic}+{created_range}&page={i}&per_page=100'
            print("GET", url)
            time.sleep(6 - min([time.time() - last_GET_time, 5]))
            last_GET_time = time.time()
            response = github_api_get(url)
            json = response.json()
            # pprint.pprint(json)
            json["url"] = response.url
            try:
                total_count = json['total_count']
            except Exception as e:
                pprint.pprint(json)
                raise
            print(total_count, i, bool((i) * 100 >= total_count))

            yield json
            if i * 100 >= total_count:
                break


def _test_json_iter():
    for json in _json_iter():
        print(json['url'])
        print(json)


def iter_repo(topic="portfolio-website"):
    que = tinydb.Query()
    urlset = set()
    for json in _json_iter(topic=topic):
        total_count, repos = json['total_count'], json['items']
        for repo in repos:
            if repo['html_url'] in urlset:
                continue
            urlset.add(repo['html_url'])
            username, reponame = repo['full_name'].split('/', maxsplit=1)
            repo['username'] = username
            repo['reponame'] = reponame
            if hash_username(repo['username']) in no_thanks:
                print('skipped', repo['full_name'])
                continue
            if not repo['homepage'] and repo['full_name'].endswith('.github.io'):
                if username == reponame.replace(".github.io", ''):
                    # such as 'umihico/umihic.github.io'
                    homepage = "https://" + reponame
                    # print('estimated', homepage)
                    repo['homepage'] = homepage
            repo['homepage_exist'] = True if repo['homepage'] else False
            yield repo


def get_repo_info(ownername, reponame):
    url = f'https://api.github.com/repos/{ownername}/{reponame}'
    pprint.pprint(requests.get(url).json())


def _test_iter_repo():
    for repo in iter_repo():
        pprint.pprint(repo)
        # raise
        html_url, description, homepage, created_at, score, stargazers_count = repo['html_url'], repo[
            'description'], repo['homepage'], repo['created_at'][:10], repo['score'], repo['stargazers_count']
        print(created_at, html_url, description, homepage, stargazers_count)


def api2location(username="umihico"):
    url = f'https://api.github.com/users/{username}'
    response = github_api_get(url)
    return response.json()['location']


def test_api2location():
    print(api2location())


def get_userlocation_rawjson(username="umihico"):
    url = f'https://api.github.com/users/{username}'
    headers = {'Accept': 'application/vnd.github.mercy-preview+json', }
    response = requests.get(url, headers=headers)
    # response.raise_for_status()
    return response.json()


def get_users_location():
    content_tinydb = load_db()
    for i, repo in enumerate(iter_repo()):
        username = repo['owner']['login']
        if not location_db.search(que.username == username):
            time.sleep(5)
            location = api2location(username)
            print(i, location)
            location_db.upsert({'username': username, 'location': location, 'tags': geotag(location),
                                'updated_at': int(time.time())}, que.username == username)


def tagble_location():
    for d in location_db.all():
        # if 'tags' in d:
        #     continue
        d['tags'] = geotag(d['location'])
        print(d['location'], d['tags'])
        location_db.upsert(d, que.username == d['username'])


def get_users_location_boost():
    rest_data = [
        ("alecmarcus", None),
        ("CheapCyborg", "Richmond, VA"),
        ("BobDempsey", "Florida!")
    ]
    for username, location in rest_data:
        d = {'username': username, 'location': location,
             'updated_at': int(time.time())}
        print(username, location)
        location_db.upsert(d, que.username == username)
    raise
    location_db.upsert()
    from proxys import proxys
    import umihico
    import threading
    import queue
    content_tinydb = load_db()
    usernames = [r['username'] for r in content_tinydb.all()
                 if not location_db.search(que.username == r['username'])]
    username_queue = queue.Queue()
    print(len(usernames))
    print(usernames)
    raise
    for username in usernames:
        username_queue.put(username)
    lock = threading.Lock()

    def get_location_proxy(proxy, username_queue, location_db, lock):
        while True:
            try:
                username = username_queue.get_nowait()
            except Exception as e:
                time.sleep(3)
                continue
            url = f'https://api.github.com/users/{username}'
            try:
                response = umihico.scraping.requests_.get(url, proxy=proxy)
                response.raise_for_status()
            except Exception as e:
                time.sleep(1000)
            if "API rate limit exceeded" in response.text:
                username_queue.put(username)
                time.sleep(10000)
            json = response.json()
            if "login" not in json:
                username_queue.put(username)
                time.sleep(1000)
                continue
            location = json['location']
            d = {'username': username, 'location': location,
                 'updated_at': int(time.time())}
            print(username, location)
            with lock:
                location_db.upsert(d, que.username == username)
    # proxys = proxys[:10]
    for proxy in proxys:
        thread = threading.Thread(target=get_location_proxy, args=(
            proxy, username_queue, location_db, lock))
        thread.start()


if __name__ == '__main__':
    # _test_created_range_iter()
    # _test_json_iter()
    # _test_iter_repo()
    # test_api2location()
    # get_users_location()
    # get_users_location_boost()
    get_users_location()
    # tagble_location()
    # get_repo_info("meetcric", "myblog")
