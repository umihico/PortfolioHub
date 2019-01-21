import requests
from PIL import Image
from io import BytesIO
import time
from chromeless import Chromeless
from selenium.webdriver import ChromeOptions
from awsgateway_credentials import awsgateway_apikey, awsgateway_url


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


def test_url_to_gif(url="http://umihi.co/", filename='test.gif'):
    url_to_gif(url, filename)


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
    starttime = time.time()
    self.get(url)
    pngs = []
    for _ in self.scroll_each_iter():
        if time.time()-starttime > 20:
            break
        pngs.append(self.get_screenshot_as_png())
    return pngs


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
        gif_success = False
        return gif_success
    images = []
    for png in pngs:
        image = Image.open(BytesIO(png))
        image.thumbnail((500, 500), Image.LANCZOS)
        images.append(image)
    gif_success = bool(images)
    if gif_success:
        images[0].save(filename, save_all=True,
                       append_images=images[1:], duration=600, loop=100, quality=30, optimize=True)
        print('saved', filename)
    return gif_success


if __name__ == '__main__':
    test_url_to_gif("https://ryanfitzgerald.github.io/devportfolio/",
                    filename="/home/umihico/git-powered-philosophy/worktree-draft/site/test.gif")
