from selenium.webdriver import Chrome, ChromeOptions
import requests
from PIL import Image
from io import BytesIO
import time


def gen_chrome():
    options = ChromeOptions()
    # options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=2160,1440')
    return Chrome(chrome_options=options)


def _gen_images_for_gif(url, chrome=None):
    while True:
        try:
            images = _gen_images_for_gif_main(url, chrome)
        except Exception as e:
            if "chrome not reachable" in str(e):
                try:
                    chrome.quit()
                except Exception as e:
                    pass
                    chrome = gen_chrome()
            else:
                raise
        else:
            return images


def _gen_images_for_gif_main(url, chrome):
    chrome = chrome or gen_chrome()
    try:
        requests.get(url, timeout=10).raise_for_status()
    except Exception as e:
        print("bad url", url)
        return False
    print("chrome.get", url)
    chrome.get(url)
    images = []
    h = 0
    for scroll in range(999):
        height = chrome.execute_script("return document.body.scrollHeight")
        if h > height:
            chrome.execute_script(f"window.scrollTo(0, {h});")
            new_height = chrome.execute_script(
                "return document.body.scrollHeight")
            if new_height == height:
                break
        png = chrome.get_screenshot_as_png()
        image = Image.open(BytesIO(png))
        image.thumbnail((500, 500), Image.LANCZOS)
        images.append(image)
        if scroll > 2:
            h += 400
        chrome.execute_script(f"window.scrollTo(0, {h});")
        time.sleep(1)
    return images


def _test(url="http://www.albinotonnina.com/"):
    filename = 'test.gif'
    url_to_gif(url, filename)


def url_to_gif(url, filename, chrome=None):
    chrome = chrome or gen_chrome()
    images = _gen_images_for_gif(url, chrome)
    if images:
        images[0].save(filename, save_all=True,
                       append_images=images[1:], duration=600, loop=100, quality=30, optimize=True)
    gif_success = True if images else False
    if gif_success:
        print('saved', filename)
    return chrome, gif_success


if __name__ == '__main__':
    chrome = gen_chrome()
    chrome.get("https://dargueta.com")
    raise
    _test(url="https://ryanfitzgerald.github.io/devportfolio")
