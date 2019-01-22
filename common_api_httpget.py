import requests
from ppickle import load
import time
last_http_time = 0
OAUTH_TOKEN = load("../OAUTH_TOKEN.json")["OAUTH_TOKEN"]


def retryable_authorized_http_requests(url):
    global last_http_time, OAUTH_TOKEN
    headers = {"Authorization": f"token {OAUTH_TOKEN}", }
    for i in range(10):
        time.sleep(max([last_http_time-time.time()+2, 0]))
        print('GET', url)
        response = requests.get(url, headers=headers)
        last_http_time = time.time()
        if 'message' not in response.json():
            return response
        else:
            print(response.json())
