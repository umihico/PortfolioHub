from api import get
from db import get_db
import time
from functools import reduce
from datetime import datetime, date


def find_repositories(optional_current_minute=None):
    conn = get_db()
    cur = conn.cursor()
    result = []
    for topic, start_year, start_month, end_year, end_month, page_index in iter_page(optional_current_minute):
        api_url = gen_url(topic, start_year, start_month,
                          end_year, end_month, page_index)
        result.append(api_url)
        url_to_database(cur, api_url)
        skip_next_page = should_skip_next_page(
            json, topic, start_year, start_month, end_year, end_month, page_index)
        if skip_next_page:
            break
    cur.close()
    conn.close()
    return result


def url_to_database(cur, url):
    json = get(url).json()
    update_database(cur, json)


def test_url_to_database():
    conn = get_db()
    cur = conn.cursor()
    url = "https://api.github.com/search/repositories?q=topic:portfolio-website+created:2020-02-01..2020-02-29&page=1&per_page=100"
    url_to_database(cur, url)


def iter_page(optional_current_minute=None):
    def get_current_minute_in_1440():
        """return int between 0 to 1439"""
        return int((time.time() % (60 * 60 * 24)) / 60)

    def iter_page_topic(topic):
        yield topic, None, None, 2016, 1
        for start_year in range(2016, 9999):
            for start_month, end_month in zip([1, 4, 7, 10], [4, 7, 10, 1]):
                if date(start_year, start_month, 1) > date.today():
                    return
                end_year = start_year if end_month > start_month else start_year + 1
                yield topic, start_year, start_month, end_year, end_month

    def _iter_page():
        for topic in ["portfolio-website", 'personal-website']:
            yield from iter_page_topic(topic)

    current_minute = get_current_minute_in_1440(
    ) if optional_current_minute is None else optional_current_minute
    for i, (topic, start_year, start_month, end_year, end_month) in enumerate(_iter_page()):
        if i == current_minute:
            for page_index in range(1, 11):
                yield topic, start_year, start_month, end_year, end_month, page_index


def test_iter_page():
    for output in iter_page():
        print(output)


def gen_url(topic, start_year, start_month, end_year, end_month, page_index):
    start_range = f"{start_year}-{str(start_month).zfill(2)}-01.." if start_year else "%3C"
    end_range = f"{end_year}-{str(end_month).zfill(2)}-01"
    return f"https://api.github.com/search/repositories?q=topic:{topic}+created:{start_range}{end_range}&page={page_index}&per_page=100"


def update_database(cur, json):
    response_to_column_mapping = {
        'id': ['id'],
        'user': ['owner', 'login'],
        'repository': ['name'],
        'repository_updated_at': ['updated_at'],
        'stars': ['stargazers_count'],
        'forks': ['forks_count'],
        'url': ['homepage'],
    }
    formatter_funcs = {
        'id': int,
        'repository_updated_at': lambda t: datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ"),
        'stars': int,
        'forks': int,
        'url': lambda url: url if url else None,
    }
    record = {}
    for repository in json['items']:
        for column, json_keys in response_to_column_mapping.items():
            record[column] = reduce(
                lambda seq, key: seq[key], json_keys, repository)
            record[column] = formatter_funcs[column](
                record[column]) if column in formatter_funcs else record[column]
        cur.execute("INSERT INTO portfolios (id, user, repository, repository_updated_at, stars, forks, url, api_fetched_at) VALUES (%(id)s, %(user)s, %(repository)s, %(repository_updated_at)s, %(stars)s, %(forks)s, %(url)s, NOW()) ON DUPLICATE KEY UPDATE id=%(id)s, user=%(user)s, repository=%(repository)s, repository_updated_at=%(repository_updated_at)s, stars=%(stars)s, forks=%(forks)s, url=%(url)s, api_fetched_at=NOW()", record)


def should_skip_next_page(json, topic, start_year, start_month, end_year, end_month, page_index):
    total_count = json["total_count"]
    items_count = len(json['items'])
    print(topic, [start_year, start_month, end_year, end_month],
          page_index, [total_count, items_count])
    if items_count < 100:
        return True
    elif total_count == page_index * 100:
        return True
    else:
        return False


if __name__ == '__main__':
    test_url_to_database()
