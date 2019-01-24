import requests
from PIL import Image
from io import BytesIO
from chromeless import Chromeless
from selenium.webdriver import Chrome, ChromeOptions
from awsgateway_credentials import awsgateway_apikey, awsgateway_url
from microdb import MicroDB
from tqdm import tqdm
import time
import sys
sys.path.append("..")
from common import jsons_dir, gifs_dir
from multiprocessing.pool import ThreadPool
import os


def gen_chrome_options():
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1366x768")
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--log-level=0")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--homedir=/tmp")
    return chrome_options


chrome_options = gen_chrome_options()


def scroll_each_iter(self):
    h = 0
    import time
    for scroll in range(999):
        height = self.execute_script("return document.body.scrollHeight")
        if h > height:
            self.execute_script(f"window.scrollTo(0, {h});")
            new_height = self.execute_script(
                "return document.body.scrollHeight")
            if new_height == height:
                break
        if scroll > 2:
            h += 400
        self.execute_script(f"window.scrollTo(0, {h});")
        time.sleep(0.5)
        yield


def scrolling_capture(self, url):
    import time
    import sys
    starttime = time.time()
    self.get(url)
    pngs = []
    image_size_sum = 0
    for _ in self.scroll_each_iter():
        if time.time()-starttime > 20:
            break
        png = self.get_screenshot_as_png()
        image_size_sum += sys.getsizeof(png)
        if image_size_sum > 6291556*0.7:
            break
        pngs.append(png)
    return pngs


def raw_pngs_to_gif(pngs, filename):
    images = []
    for png in pngs:
        image = Image.open(BytesIO(png))
        image.thumbnail((500, 500), Image.LANCZOS)
        images.append(image)
    gif_success = bool(images)

    if gif_success:
        images[0].save(filename, save_all=True,
                       append_images=images[1:], duration=600, loop=100, quality=30, optimize=True)
        try:
            Image.open(filename)
        except Exception as e:
            os.remove(filename)
            gif_success = False
    return gif_success


def url_to_gif(url, filename):
    try:
        requests.get(url, timeout=10).raise_for_status()
    except Exception as e:
        gif_success = False
        return gif_success
    chrome = Chromeless(awsgateway_url, awsgateway_apikey, chrome_options=chrome_options)
    chrome.attach_method(scrolling_capture)
    chrome.attach_method(scroll_each_iter)
    try:
        pngs = chrome.scrolling_capture(url)
    except Exception as e:
        print(e)
        print('failed', url)
        gif_success = False
        return gif_success
    return raw_pngs_to_gif(pngs, filename)


def url_to_gif_locally(url, filename):
    Chrome.scrolling_capture = scrolling_capture
    Chrome.scroll_each_iter = scroll_each_iter
    chrome = Chrome(chrome_options=chrome_options)
    pngs = chrome.scrolling_capture(url)
    [print(sys.getsizeof(png)) for png in pngs]
    # 1290681
    # 1299371
    # 1304405
    # 604651
    # 803958
    # 834891
    # 150128
    # 530121
    # 367501
    # 84065
    # 123281
    # 123281
    # 123281
    print(sys.getsizeof(pngs))
    # 192
    raw_pngs_to_gif(pngs, filename)
    chrome.quit()


def gen_filename(repo):
    full_name = repo['full_name']
    return gifs_dir + full_name.replace('/', '-').lower() + '.gif'


def gen_gif_json(last_try, scrapped_at, full_name, success, filepath,):
    gif_json = {
        'last_try': last_try,
        'scrapped_at': scrapped_at,
        'full_name': full_name,
        'success': success,
        'filepath': filepath,
    }
    return gif_json


def update(mdb_gifs, repo):
    filepath = gen_filename(repo)
    url = repo['homepage']
    gif_success = url_to_gif(url, filepath)
    gif_json = gen_gif_json(time.time(), repo['pushed_at'],
                            repo['full_name'], gif_success, filepath)
    mdb_gifs.upsert(gif_json)
    mdb_gifs.save()


def exact_update_required(mdb_repos, mdb_gifs):
    def is_update_required(repo):

        if not repo['homepage']:
            return False
        if repo not in mdb_gifs:
            return True
        gif_json = mdb_gifs.get(repo)
        """optional"""
        # if not gif_json['success']:
        #     return True
        if gif_json['success'] and not os.path.exists(gif_json['filepath']):
            return True
        """optional end """
        if time.time() < gif_json['last_try']+3*60*60*24:
            return False
        if repo['pushed_at'] == gif_json['scrapped_at']:
            return True
        else:
            return False
    update_required_repos = []
    for repo in mdb_repos.all():
        if is_update_required(repo):
            update_required_repos.append(repo)
        else:
            current_gif_json = mdb_gifs.get(repo, {})
            last_try = current_gif_json.get('last_try', 0)
            scrapped_at = current_gif_json.get('scrapped_at', None)
            full_name = repo['full_name']
            success = current_gif_json.get('success', False)
            filepath = current_gif_json.get('filepath', None)
            gif_json = gen_gif_json(last_try, scrapped_at, full_name, success, filepath)
            mdb_gifs.upsert(gif_json)
    mdb_gifs.save()
    return update_required_repos


def update_mutlitherading_wrapper(args):
    mdb_gifs, repo = args
    return update(mdb_gifs, repo)


def scrap_repos():
    mdb_repos = MicroDB(jsons_dir+'repos.json', partition_keys=['full_name', ])
    mdb_gifs = MicroDB(jsons_dir+'gifs.json', partition_keys=['full_name', ])
    update_required_repos = exact_update_required(mdb_repos, mdb_gifs)
    args_iterable = [(mdb_gifs, repo) for repo in update_required_repos]
    with ThreadPool(processes=20) as pool:
        for _ in tqdm(pool.imap_unordered(update_mutlitherading_wrapper, args_iterable), total=len(update_required_repos)):
            pass


def del_invalid_gifs():
    for gif_filename in os.listdir(gifs_dir):
        gif_path = gifs_dir+gif_filename
        try:
            Image.open(gif_path)
        except Exception as e:
            print(gif_path)
            os.remove(gif_path)


if __name__ == '__main__':
    # del_invalid_gifs()
    scrap_repos()
    # url_to_gif("https://shawnblakesley.github.io/",
    #            filename="/home/umihico/git-powered-philosophy/worktree-draft/site/test.gif")
