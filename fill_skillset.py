from api import get
from db import get_db
import time
import json
from pprint import pprint


def fill_skillset():
    conn = get_db()
    cur = conn.cursor()
    usernames = select_targets(cur)
    if len(usernames) == 0:
        return 'zero'
    username = usernames[0]
    skill_set_dict = username_to_skills(username, cur)
    print(username, skill_set_dict)
    update_database(username, skill_set_dict, cur)
    return {'username': username, 'skill_set_dict': skill_set_dict}


def select_targets(cur):
    cur.execute("select user from portfolios where gif is not null and ( skills_updated_at<date_sub(curdate(), interval 10 day) or skills_updated_at is null) order by datediff(repository_updated_at, ifnull(skills_updated_at,  STR_TO_DATE('1900,1,1','%Y,%m,%d'))) desc limit 100")
    return list(set([record[0] for record in cur.fetchall()]))


def username_to_skills(username, cur):
    url = f'https://api.github.com/users/{username}/repos?per_page=100&page=1&sort=pushed'
    try:
        res = get(url)
        res.raise_for_status()
    except Exception:
        if res.status_code == 404:
            cur.execute(
                "DELETE FROM portfolios WHERE user = %(user)s",
                {'user': username}
            )
        else:
            pprint(res.json())
            print('status_code', res.status_code)
            raise
    return calc_skillset(res.json())


class RepositoryScore():
    def __init__(self, name, language, size):
        self.name = name
        self.language = language
        self.size = size
        self.date_point = None
        self.size_point = None
        self.total_point = None


def calc_skillset(raw_repositories):
    if 'message' in raw_repositories and raw_repositories['message'] == 'Not Found':
        return {}
    self_repositories = [r for r in raw_repositories if not r['fork']]
    has_lang_repositories = [
        r for r in self_repositories if r['language'] is not None]
    repositories = [RepositoryScore(r['name'], r['language'], r['size'])
                    for r in has_lang_repositories]
    for date_point, repo in enumerate(reversed(repositories), start=1):
        repo.date_point = date_point
    sizes = [r.size for r in repositories]
    size_to_points_dict = {size: p for p,
                           size in enumerate(sorted(sizes), start=1)}
    for repo in repositories:
        repo.size_point = size_to_points_dict[repo.size]
    for repo in repositories:
        repo.total_point = repo.size_point * repo.date_point
    lang_point_sum_dict = {}
    for repo in repositories:
        lang = repo.language
        lang_point_sum_dict[lang] = lang_point_sum_dict.get(
            lang, 0) + repo.total_point
    total = sum(lang_point_sum_dict.values())
    if total == 0:
        return {}
    for key in lang_point_sum_dict:
        lang_point_sum_dict[key] = int(
            (lang_point_sum_dict[key] * 100) / total)
    lang_point_sum_dict = {lang: size for lang,
                           size in lang_point_sum_dict.items() if size > 0}
    return lang_point_sum_dict


def update_database(username, skill_set_dict, cur):
    record = {"skills": json.dumps(skill_set_dict), "skills_updated_at": time.strftime(
        '%Y-%m-%d %H:%M:%S'), "user": username}
    cur.execute(
        'UPDATE portfolios SET skills=%(skills)s, skills_updated_at=%(skills_updated_at)s WHERE user=%(user)s', record)


if __name__ == '__main__':
    fill_skillset()
