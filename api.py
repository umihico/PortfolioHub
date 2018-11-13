
import requests
import pprint
import time
import datetime


def _created_range_iter():
    for year in range(2014, 9999):
        for month in [1, 4, 7, 10]:
            today = datetime.date.today()
            if datetime.datetime(year, month, 1) > datetime.datetime(today.year, today.month, today.day):
                raise StopIteration
            end_year = year if month != 10 else year + 1
            end_month = month + 3 if month != 10 else 1
            created_range = f"created:{year}-{str(month).zfill(2)}-01..{end_year}-{str(end_month).zfill(2)}-01"
            yield created_range


def _test_created_range_iter():
    for created_range in _created_range_iter():
        print(created_range)


def github_api_get(url):
    headers = {
        'Accept': 'application/vnd.github.mercy-preview+json', }
    while True:
        response = requests.get(url, headers=headers)
        json = response.json()
        if 'message' in json and "API rate limit exceeded for " in json['message']:
            print("API rate limit exceeded")
            time.sleep(20)
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

            yield json
            if i > total_count // 100:
                break


def _test_json_iter():
    for json in _json_iter():
        print(json['url'])
        print(json)


def iter_repo(topic="portfolio-website"):
    urlset = set()
    for json in _json_iter():
        total_count, repos = json['total_count'], json['items']
        for repo in repos:
            if repo['html_url'] in urlset:
                continue
            urlset.add(repo['html_url'])
            if repo['homepage']:
                yield repo
            else:
                print("no homepage", repo['html_url'])


def _test_iter_repo():
    for repo in iter_repo():
        html_url, description, homepage, created_at, score, stargazers_count = repo['html_url'], repo[
            'description'], repo['homepage'], repo['created_at'][:10], repo['score'], repo['stargazers_count']
        print(created_at, html_url, description, homepage, stargazers_count)


if __name__ == '__main__':
    # _test_created_range_iter()
    # _test_json_iter()
    _test_iter_repo()
