import sys
import time
from tqdm import tqdm
sys.path.append("..")
from common import retryable_authorized_http_requests, jsons_dir
from microdb import MicroDB


def username_to_skills(username="umihico"):
    url = f'https://api.github.com/users/{username}/repos?per_page=100&page=1&sort=pushed'
    repositories = retryable_authorized_http_requests(url).json()
    self_repositories = [r for r in repositories if not r['fork']]
    langs_and_sizes = [(r['language'], r['size']) for r in self_repositories]
    weights = [1+1/i for i in range(1, 102)]
    langs_and_adjusted_sizes = [(lang, size*wei)
                                for wei, (lang, size) in zip(weights, langs_and_sizes)]
    lang_sum_dict = {}
    for lang, size in langs_and_adjusted_sizes:
        if lang:
            lang_sum_dict[lang] = lang_sum_dict.get(lang, 0)+size
    total = sum(lang_sum_dict.values())
    for key in lang_sum_dict:
        lang_sum_dict[key] = int((lang_sum_dict[key]*100)/total)
    lang_sum_dict = {lang: size for lang, size in lang_sum_dict.items() if size > 0}
    lang_list = list(sorted(lang_sum_dict.items(), key=lambda x: x[1], reverse=True))
    return lang_list


def test_username_to_skills():
    print(username_to_skills())
    # [('Python', 50), ('HTML', 49)]


def update(username, mdb_skills):
    skills = username_to_skills(username)
    skill_json = {
        "username": username,
        'last_modified': time.time(),
        'skills': skills,
    }
    print(username, skills)
    mdb_skills.upsert(skill_json)
    mdb_skills.save()


def sort_by_priotity(mdb_repos, mdb_skills):
    last_modified_time_dict = {}
    for repo in mdb_repos.all():
        username = repo['username']
        if repo in mdb_skills:
            skill_json = mdb_skills.get(repo)
            last_modified = skill_json['last_modified']
        else:
            # print(username)
            last_modified = 0
            skill_json = {}
        last_modified_time_dict[username] = last_modified
    usernames_times = list(last_modified_time_dict.items())
    usernames_times.sort(key=lambda x: x[1])
    usernames = [username for username, time_ in usernames_times]
    return usernames


def attach_all_skills(upto=100):
    mdb_repos = MicroDB(jsons_dir+'repos.json', partition_keys=['username', ])
    mdb_skills = MicroDB(jsons_dir+'skills.json', partition_keys=['username', ])
    sorted_usernames_by_priotity = sort_by_priotity(mdb_repos, mdb_skills)
    for username in tqdm(sorted_usernames_by_priotity[:upto]):
        update(username, mdb_skills)


if __name__ == '__main__':
    # test_username_to_skills()
    attach_all_skills(100)
