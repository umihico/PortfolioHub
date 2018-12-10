import requests


def star_repo(full_name):
    return
    url = f"http://api.github.com//user/starred/{full_name}"
    headers = {"Content-Length": '0'}
    response = requests.put(url, headers=headers)
    print(response.text)


if __name__ == '__main__':
    star_repo("Meuss/portfolio")
