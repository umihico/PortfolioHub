import requests
import os
import env
import time

headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}", }


def get(url, slept_recursive_count=0):
    print("GET", url)
    start = time.time()
    res = requests.get(url, headers=headers)
    print("GET took", time.time() - start)
    return res


if __name__ == '__main__':
    test_url = "https://api.github.com/search/repositories?q=topic:portfolio-website+created:2019-07-01..2019-10-01&page=1&per_page=100"
    json = get(test_url).json()
    print(json)
    # run in terminal "GITHUB_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx python api.py"
