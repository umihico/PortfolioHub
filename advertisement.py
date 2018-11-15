import umihico
apikey = umihico._set_env_value("github_adv", optional_value=None)
import requests
from common import content_tinydb


def send_star_all():
    for repo in content_tinydb.all():
        if repo["stargazers_count"] > 0:
            continue
        username, reponame = repo["full_name"].split('/', 1)


def send_star(username, reponame):
    url = f"https://api.github.com/user/starred/{username}/{reponame}"
    requests.post(url, data=None, json=None)
    session = requests.session(auth=("umihico", apikey))
    # Create our issue
    # issue = {'title': title,
    #          'body': body,
    #          'assignee': assignee,
    #          'milestone': milestone,
    #          'labels': labels}
    # Add the issue to our repository
    r = session.post(url)


def test_send_star():
    send_star("umihico", "minigun-requests")


if __name__ == '__main__':
    test_send_star()
