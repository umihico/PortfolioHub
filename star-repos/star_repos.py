
import sys
sys.path.append('..')
from common_api_httpget import headers
from microdb import MicroDB
import requests
from tqdm import tqdm
from time import sleep
headers = headers.copy()
headers.update({"Content-Length": "0", })


def star_one_repo(repo):
    full_name = repo['full_name']
    sleep(2)
    url = f"https://api.github.com/user/starred/{full_name}"
    print(full_name)
    response = requests.put(url, headers=headers)
    print(response.status_code)
    if response.status_code != 204:
        print(response.headers)
        print(response.text)


# def test_star_one_repo():

def exact_yet_stared_succeed_repos():
    mdb_repos = MicroDB('../listup-repo/repos.json', partition_keys=['full_name', ])
    mdb_gifs = MicroDB('../scrap-repo/gifs.json', partition_keys=['full_name', ])
    yet_stared_succeed_repos = []
    for d in mdb_repos.all():
        gifjson = mdb_gifs.get(d)
        if gifjson['success'] and d['stargazers_count'] == 0:
            yet_stared_succeed_repos.append(d)
    return yet_stared_succeed_repos


def star_all_repo():
    yet_stared_succeed_repos = exact_yet_stared_succeed_repos()
    for repo in tqdm(yet_stared_succeed_repos):
        star_one_repo(repo)


if __name__ == '__main__':
    star_all_repo()
