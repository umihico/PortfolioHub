import requests
from ppickle import load
import time
last_http_time = 0
OAUTH_TOKEN = load("../token.json")["OAUTH_TOKEN"]
headers = {"Authorization": f"token {OAUTH_TOKEN}", }


def retryable_authorized_http_requests(url):
    global last_http_time, headers
    for i in range(10):
        time.sleep(max([last_http_time-time.time()+2, 0]))
        print('GET', url)
        response = requests.get(url, headers=headers)
        last_http_time = time.time()
        if 'message' not in response.json():
            return response
        else:
            print(response.json())
            if response.json()["message"] == 'Not Found':
                return response


from subprocess import check_output
current_branch_name = check_output(
    "git symbolic-ref --short HEAD".split(" ")).decode().split('\n')[0]

topic = "portfolio-website"
if current_branch_name == 'personal-website':
    topic = 'personal-website'


htmls_root_dir = "../../thumbnailed-portfolio-websites/"
if current_branch_name == 'personal-website':
    htmls_root_dir = "../../thumbnailed-personal-websites/"

jsons_dir = htmls_root_dir+'jsons/'
gifs_dir = htmls_root_dir+'gifs/'
