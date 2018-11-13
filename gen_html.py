from flask_frozen import Freezer
from flask import Flask, render_template, redirect, url_for
from common import html_dir, load_db, chunks, gen_filename, numberize_int
app = Flask(__name__)

path_data_dict = {}


@app.route('/')
def top():
    return redirect('/most_stars0001.html')


@app.route('/<path>/')
# def test2_dynamic_path(path="index"):
#     return render_template('./test_dynamic.html', value=path)
def index(path):
    headline_menu, tabulated_repos, max_page_num = path_data_dict[path]
    pagenation_bar = gen_pagenation_bar(path, max_page_num)
    return render_template(
        'templete.html',
        headline_menu=headline_menu,
        tabulated_repos=tabulated_repos,
        pagenation_bar=pagenation_bar)


def gen_pagenation_bar(path, max_page_num):
    # path="most_stars0001.html"
    current_page = numberize_int(path)
    filename = path.replace(str(current_page).zfill(4) + ".html", "")
    page_nums = gen_page_nums(current_page, max_page_num)
    pagenation_bar = [(num, gen_html_filename(filename, num), not bool(
        num == current_page or num == '...')) for num in page_nums]
    return pagenation_bar


def gen_page_nums(current_page, max_page_num):
    middle_page_num = current_page if bool(
        3 <= current_page <= max_page_num - 2) else 3 if current_page < 3 else max_page_num - 2
    n = middle_page_num
    middle_nums = [n - 2, n - 1, n, n + 1, n + 2]
    if middle_nums[0] > 1:
        middle_nums.insert(0, 1)
    if middle_nums[1] > 2:
        middle_nums.insert(1, '...')

    if middle_nums[-1] < max_page_num:
        middle_nums.append(max_page_num)
    if middle_nums[-2] < max_page_num - 1:
        middle_nums.insert(-1, '...')
    return middle_nums


def test_gen_pagenation_bar():
    test_nums = [
        (1, 100),
        (2, 100),
        (3, 100),
        (4, 100),
        (50, 100),
        (96, 100),
        (97, 100),
        (98, 100),
        (99, 100),
        (100, 100),
    ]
    for test_num in test_nums:
        print(test_num)
        print(gen_page_nums(*test_num))
    for test_num in test_nums:
        path = gen_html_filename('most_stars', test_num[0])
        print(test_num)
        print(gen_pagenation_bar(path, test_num[1]))


def build_static_files(paths):
    freezer = Freezer(app)
    app.config['FREEZER_RELATIVE_URLS'] = True
    app.config['FREEZER_DESTINATION'] = html_dir
    app.config['FREEZER_DESTINATION_IGNORE'] = ["gifs", ]

    @freezer.register_generator
    def product_url_generator():
        for path in paths:
            print(path)
            yield "/" + path
    freezer.freeze()


def gen_html_filename(filename, page_index):
    return filename + str(page_index).zfill(4) + '.html'


def render_static_files():
    for filename, page_index, headline_menu, tabulated_repos, max_page_num in iter_page_data():
        path_data_dict[gen_html_filename(filename, page_index)] = (
            headline_menu, tabulated_repos, max_page_num)
    paths = list(path_data_dict.keys())
    build_static_files(paths)


def iter_page_data():
    """
    *in templete.html*
    for tr_repos in tabulated_repos:
        for filename, tubled_inforows in tr_repost:
            for string,url ,do_herfin tubled_inforow:
    """
    content_tinydb = load_db()
    all_repo = content_tinydb.all()
    sortkey_dict = {'most_stars': "stargazers_count",
                    'most_forks': "forks",
                    'recently_updated': "updated_at", }
    for filename, headline_menu in iter_headline():
        sortkey = sortkey_dict[filename]
        all_repo.sort(key=lambda repo: repo[sortkey], reverse=True)
        chunked_repos = chunks(all_repo, 9)
        max_page_num = len(chunked_repos)
        for page_index, nine_repo in enumerate(chunked_repos):
            tubled_inforows = [to_tubled_inforow(repo) for repo in nine_repo]
            tubled_inforows = [x for x in tubled_inforows if x]
            tabulated_repos = chunks(tubled_inforows, 3)
            yield filename, page_index + 1, headline_menu, tabulated_repos, max_page_num


def to_tubled_inforow(repo):
    """for string,url,do_herf in tubled_inforow"""
    if 'homepage' not in repo:
        print('no homepage', repo['html_url'])
        repo['homepage'] = ''
    tubled_inforow = []
    tubled_inforow.append(
        ('GitHub:' + repo['full_name'], repo['html_url'], True))
    tubled_inforow.append(('portfolio website', repo['homepage'], True))
    tubled_inforow.append(
        (f"{repo['stargazers_count']} stars", repo['html_url'] + '/stargazers', True))
    tubled_inforow.append(
        (f"{repo['forks']} forks", repo['html_url'] + '/network/members', True))
    tubled_inforow.append(
        ("updated:" + str(repo['updated_at'])[:10], '', False))
    gif_filename = gen_filename(repo['full_name'])
    td = [gif_filename, tubled_inforow]
    return td


def iter_headline():
    # {"full_name":"itsdpm\/itsdpm.github.io","html_url":"https:\/\/github.com\/itsdpm\/itsdpm.github.io","description":"Website hosted at -- ","created_at":"2017-12-10T10:48:16Z","updated_at":"2017-12-10T13:39:21Z","size":1,"stargazers_count":0,"watchers_count":0,"forks":0,"watchers":0,"score":4.102341,"gif_success":true}
    headline_menus_strings_keys = [('Most stars', "most_stars"),
                                   ('Most forks', "most_forks"), ('Recently updated', "recently_updated"), ]
    for iter_key, url in headline_menus_strings_keys:
        headline_menu = [(url + '0001.html', key, bool(key == iter_key))
                         for key, url in headline_menus_strings_keys]
        yield url, headline_menu


def test_build_static_files():
    paths = ['/a/', '/b/']
    build_static_files(paths)


if __name__ == "__main__":
    # app.run()
    # test_build_static_files()
    render_static_files()
    # test_gen_pagenation_bar()
