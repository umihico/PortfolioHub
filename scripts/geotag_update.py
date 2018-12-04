# messed up
import requests
import tqdm
import time
from common import DictTinyDB, db, html_dir

ldb = DictTinyDB(
    html_dir + 'location.json', 'username')


def geotag_update():
    should_update_usernames = [
        d['username'] for d in db.all() if d['homepage_exist'] and d['gif_success']
    ]
    print(len(should_update_usernames))
    lasttime_update_dict = {d['username']: d['updated_at']
                            for d in ldb.all()}
    should_update_usernames.sort(
        key=lambda name: lasttime_update_dict.get(name, 0))
    for username, location in iter_json_till_error(should_update_usernames):
        d = {'username': username,
             'location': location, 'updated_at': int(time.time())}
        ldb.upsert(d)


def iter_json_till_error(usernames):
    for username in tqdm.tqdm(usernames):
        time.sleep(1)
        location = get_location(username)
        print(location)
        if location or location is None:
            yield username, location
        else:
            raise StopIteration()


def get_location(username="umihico"):
    url = f'https://api.github.com/users/{username}'
    headers = {'Accept': 'application/vnd.github.mercy-preview+json', }
    response = requests.get(url, headers=headers)
    try:
        response.raise_for_status()
        json = response.json()
        location = json['location']
    except Exception as e:
        if "API rate limit exceeded" in response.text:
            print("API rate limit exceeded")
            return False
        if "Not Found" in response.text:
            print(username, "Not Found")
            return None
        else:
            print(username)
            print(response.text)
            raise Exception('unknown response') from e
    else:
        return location


def test_get_location():
    print(get_location(username="umihico"))


if __name__ == '__main__':
    # test_get_location()
    geotag_update()
