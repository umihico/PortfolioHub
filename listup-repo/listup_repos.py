import datetime
from is_no_thanks_user import is_no_thanks_user
from microdb import MicroDB
import sys
sys.path.append("..")
from common import retryable_authorized_http_requests, jsons_dir, topic


def get_repos(url):
    response = retryable_authorized_http_requests(url)
    json = response.json()
    print('total_count', json['total_count'])
    repo_list = json['items']
    return repo_list


def iter_season_url():
    for start_year in range(2014, 9999):
        for start_month in [1, 4, 7, 10]:
            if datetime.date(start_year, start_month, 1) > datetime.date.today():
                raise StopIteration
            end_month = start_month+3
            end_year = start_year
            if end_month > 12:
                end_month -= 12
                end_year += 1
            start_month = str(start_month).zfill(2)
            end_month = str(end_month).zfill(2)
            created_range = f"created:{start_year}-{start_month}-01..{end_year}-{end_month}-01"
            url = f'https://api.github.com/search/repositories?q=topic:{topic}+{created_range}'
            yield url


def iter_page(season_query_url):
    for i in range(1, 11):
        final_query_url = season_query_url+f"&page={i}&per_page=100"
        yield final_query_url


def get_all_repos():
    all_repos = []
    for season_query_url in iter_season_url():
        for final_query_url in iter_page(season_query_url):
            repos = get_repos(final_query_url)
            if repos:
                all_repos.extend(repos)
            else:
                break  # break paging and goto next season
        #     break
        # break
    return all_repos


def trim_repos(all_repos):
    def trim_repo(repo):
        username, reponame = repo['full_name'].split('/', maxsplit=1)
        repo['username'] = username
        repo['reponame'] = reponame
        if not repo['homepage'] and username == reponame.replace(".github.io", ''):
            repo['homepage'] = "https://" + reponame
        valid_keys = ['username', 'reponame', "html_url", 'stargazers_count',
                      'homepage', 'forks', 'full_name', 'created_at', 'pushed_at']
        repo = {k: v for k, v in repo.items() if k in valid_keys}
        for key in valid_keys:
            if key not in repo:
                print(repo)
        return repo
    all_repos = [trim_repo(repo) for repo in all_repos]
    return all_repos


def exclude_no_thanks(repos):
    new_repos = []
    for repo in repos:
        if is_no_thanks_user(repo['username']):
            print("skip", repo['username'])
        else:
            new_repos.append(repo)
    return new_repos


def save_all_repos():
    all_repos = get_all_repos()
    all_repos = trim_repos(all_repos)
    all_repos = exclude_no_thanks(all_repos)
    mdb = MicroDB(jsons_dir+'repos.json', partition_keys=['full_name', ])
    for repo in all_repos:
        mdb.upsert(dictionary=repo)
    mdb.save()


if __name__ == '__main__':
    save_all_repos()
