from db import get_db
import os
import tempfile
from PIL import Image
import requests
import hashlib
from io import BytesIO
import time
from selenium.webdriver import Chrome, ChromeOptions
import sys
import boto3
import traceback


class PanoramicScreenCapturingChrome(Chrome):
    def __init__(self):
        executable_path = "chromedriver" if os.getenv(
            "ENV", "local") == "local" else "/opt/python/bin/chromedriver"
        super().__init__(executable_path=executable_path, options=self.get_headless_option())

    def get_headless_option(self):
        chrome_options = ChromeOptions()
        for option in ["--headless", "--disable-gpu", "--window-size=1366x768", "--disable-application-cache", "--disable-infobars", "--no-sandbox", "--hide-scrollbars", "--enable-logging", "--log-level=0", "--single-process", "--ignore-certificate-errors", "--homedir=/tmp"]:
            chrome_options.add_argument(option)
        if os.getenv("ENV", "local") != "local":
            chrome_options.binary_location = "/opt/python/bin/headless-chromium"
        return chrome_options

    def scroll_down(self):
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

    def capture_pngs(self):
        starttime = time.time()
        pngs = []
        image_size_sum = 0
        for _ in self.scroll_down():
            if time.time() - starttime > 20:
                break
            png = self.get_screenshot_as_png()
            image_size_sum += sys.getsizeof(png)
            image = Image.open(BytesIO(png))
            image.thumbnail((500, 500), Image.LANCZOS)
            pngs.append(image)
        return pngs


def screenshot_portfolios():
    conn = get_db()
    url = select_target(conn)
    if url is None:
        return None
    pre_update_database(url, conn)
    result_dict = screenshot_portfolio(url)
    update_database(result_dict, conn)
    return result_dict


def select_target(conn):
    records = get_all_target(conn)
    urls = list(set([record[0] for record in records]))
    return urls[0] if len(urls) else None


def get_all_target(conn):
    cur = conn.cursor()
    cur.execute("select url from portfolios where url is not null and ( (gif_updated_at<date_sub(curdate(), interval 3 day) and repository_updated_at>gif_updated_at) or gif_updated_at is null) order by datediff(repository_updated_at, ifnull(gif_updated_at,  STR_TO_DATE('1900,1,1','%Y,%m,%d'))) desc limit 100")
    records = cur.fetchall()
    return records


def test_select_target():
    conn = get_db()
    recrods = select_target(conn)
    users = [r[1] for r in recrods]
    print(users)


def screenshot_portfolio(url):
    result_dict = {"url": url}
    gif_filename = gen_filename(url)
    print(url, gif_filename)
    try:
        process_name = 'requests.get'
        requests.get(url, timeout=10).raise_for_status()
        process_name = 'chrome'
        chrome = PanoramicScreenCapturingChrome()
        try:
            chrome.get(url)
            pngs = chrome.capture_pngs()
        except Exception:
            raise
        finally:
            chrome.quit()
        if len(pngs) == 0:
            process_name = 'zero_pngs'
            raise
        process_name = 'pngs_to_gif'
        with tempfile.TemporaryDirectory() as tmpdir:
            pngs_to_gif(pngs, gif_filename, tmpdir)
            upload_gif(gif_filename, tmpdir)
        result_dict['filename'] = gif_filename
        result_dict['success'] = True
    except Exception:
        result_dict['success'] = False
        traceback.print_exc()
        print(process_name)
        result_dict['error_detail'] = process_name
    finally:
        return result_dict


def gen_filename(url):
    return hashlib.sha256(url.encode('utf-8')).hexdigest() + ".gif"


def pngs_to_gif(pngs, filename, tmpdir):
    fullpath = tmpdir + '/' + filename
    print(fullpath)
    pngs[0].save(fullpath, save_all=True,
                 append_images=pngs[1:], duration=600, loop=100, quality=30, optimize=True)
    Image.open(fullpath)


def upload_gif(gif_filename, tmpdir):
    fullpath = tmpdir + '/' + gif_filename
    s3 = boto3.session.Session(profile_name='umihico').resource(
        's3') if os.getenv("ENV", "local") == "local" else boto3.resource('s3')
    bucket = s3.Bucket('portfoliohub')
    bucket.upload_file(fullpath, gif_filename)


def update_database(result_dict, conn):
    if "filename" not in result_dict:
        result_dict["filename"] = None
    if "error_detail" not in result_dict:
        result_dict["error_detail"] = None
    cur = conn.cursor()
    cur.execute('UPDATE portfolios SET gif=%(filename)s, gif_updated_at=NOW(), error_detail=%(error_detail)s WHERE url=%(url)s', result_dict)


def pre_update_database(url, conn):
    cur = conn.cursor()
    cur.execute(
        'UPDATE portfolios SET gif=null, gif_updated_at=NOW(), error_detail="start_processing" WHERE url=%(url)s', {"url": url})


if __name__ == '__main__':
    screenshot_portfolios()
