from flask_frozen import Freezer
from flask import Flask, render_template, redirect
from common import html_dir, db, chunks, gen_filename, numberize_int, que, raise_with_printed_args, get_username, save_as_txt, load_from_txt
import collections
app = Flask(__name__)

path_data_dict = {}

headline_menus_strings_keys = [('Most stars', "most_stars"),
                               ('Most forks', "most_forks"), ('Recently updated', "recently_updated"), ]
deactivated_headline = [(url + '0001.html', key, False)
                        for key, url in headline_menus_strings_keys]


def css_write():
    with open('templates/css.css', mode='r') as r:
        with open('../umihico.github.io/thumbnailed-portfolio-websites/css.css', mode='w') as w:
            w.write(r.read())


def gen_tags():
    chained_location_tags = []
    for d in db.all():
        if 'userdict' in d and d['gif_success'] and d['homepage_exist']:
            chained_location_tags.extend(d['userdict']['tags'])
    counted_tagdict = collections.Counter(chained_location_tags)
    # Counter({'a': 4, 'c': 2, 'b': 1})
    tags_counts = sorted(list(counted_tagdict.items()),
                         key=lambda x: x[1], reverse=True)
    return tags_counts


tags_info = gen_tags()


@app.route('/<path>/')
def index(path):
    if path == 'database.html':
        return alluser()
    headline_menu, chunked_repos, max_page_num, tags_num = path_data_dict[path]
    pagenation_bar = gen_pagenation_bar(path, max_page_num)
    return render_template(
        'templete.html',
        tags_info=tags_info,
        tags_num=tags_num,
        headline_menu=headline_menu,
        repos=chunked_repos,
        pagenation_bar=pagenation_bar,
        grid=True,
        non_grid_rows=None)


@app.route('/')
def top():
    return redirect('/most_stars0001.html')


def alluser():
    non_grid_rows = []
    non_grid_rows.append([(x, False, x) for x in ['name', 'repository', 'star', 'fork',
                                                  'website', 'valid url', 'gif success', 'updated_at', 'gif', 'locations']])
    for d in db.all():
        full_name = d['full_name']
        repourl = 'https://github.com/' + d['full_name']
        name = d['username']
        star = d['stargazers_count']
        forks = d['forks']
        homepage = d['homepage']
        homepage_exist = d['homepage_exist']
        gif_success = d.get('gif_success', 'not tried')
        updated_at = d['updated_at'][:10]
        locations = ','.join(
            d.get('userdict', {}).get('tags', []))
        locations = locations if locations else 'None'
        gif_url = gen_filename(d['full_name'])
        tr = []
        for x in [name, repourl, star, forks, homepage,
                  homepage_exist, gif_success, updated_at, gif_url, locations]:
            value = 'website' if x == homepage else 'gif' if x == gif_url else 'repository' if x == repourl else x
            href_bool = bool(value in ['website', 'gif', 'repository'])
            if x == homepage and x is None:
                href_bool = False
            tr.append((value, href_bool, x))
        non_grid_rows.append(tr)
    for tr in non_grid_rows:
        # print(tr)
        for value, do_href, url in tr:
            pass
    # print(non_grid_rows[0][2][0])
    non_grid_rows.sort(
        key=lambda x: 999999 if x[2][0] == 'star' else x[2][0], reverse=True)
    return render_template(
        'templete.html',
        tags_info=tags_info,
        tags_num=30,
        headline_menu=deactivated_headline,
        repos=[],
        pagenation_bar=list(),
        grid=False,
        non_grid_rows=non_grid_rows)


@raise_with_printed_args
def gen_pagenation_bar(path, max_page_num):
    if path == 'locations.html':
        return []
    # path="most_stars0001.html"
    current_page = numberize_int(path)
    filename = path.replace(str(current_page).zfill(4) + ".html", "")
    page_nums = gen_page_nums(current_page, max_page_num)
    pagenation_bar = [(num, gen_html_filename(filename, num), not bool(
        num == current_page or num == '...')) for num in page_nums]
    return pagenation_bar


@raise_with_printed_args
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
    middle_nums = [x for x in middle_nums if x ==
                   '...' or 0 < x <= max_page_num]
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


@raise_with_printed_args
def build_static_files(paths):
    freezer = Freezer(app)
    app.config['FREEZER_RELATIVE_URLS'] = False
    app.config['FREEZER_DESTINATION'] = html_dir
    app.config['FREEZER_DESTINATION_IGNORE'] = ["gifs", ]

    @freezer.register_generator
    def product_url_generator():
        for path in paths:
            print("writing", path)
            yield "/" + path
    freezer.freeze()


def gen_html_filename(filename, page_index):
    if str(page_index) == '0':
        return filename + '.html'
    else:
        return filename + str(page_index).zfill(4) + '.html'


@raise_with_printed_args
def render_static_files():
    css_write()
    for filename, page_index, headline_menu, chunked_repos, max_page_num, tags_num in iter_page_data():
        print("calculating", filename, page_index)
        path_data_dict[gen_html_filename(filename, page_index)] = (
            headline_menu, chunked_repos, max_page_num, tags_num)
    paths = list(path_data_dict.keys())
    paths.append('database.html')
    build_static_files(paths)


def mention_users_in_issue(usernames):
    for chunked_usernames in chunks(usernames, 50):
        text = ' '.join(['@' + n for n in chunked_usernames])
        print(text)
        print()
        print()
        print()


def gen_current_users():
    all_repo = content_tinydb.all()
    current_users = [get_username(r['full_name'])
                     for r in all_repo if r['gif_success']]
    save_as_txt('current_users.txt', current_users)


@raise_with_printed_args
def iter_page_data():
    """
    *in templete.html*
    for tr_repos in tabulated_repos:
        for filename, tubled_inforows in tr_repost:
            for string,url ,do_herfin tubled_inforow:
    """
    all_repo = db.all()
    all_repo = [
        r for r in all_repo if 'homepage_exist' in r and r['homepage_exist'] and r['gif_success']]
    sortkey_dict = {'most_stars': "stargazers_count",
                    'most_forks': "forks",
                    'recently_updated': "updated_at", }
    for filename, headline_menu in iter_headline():
        sortkey = sortkey_dict[filename]
        all_repo.sort(key=lambda repo: repo[sortkey], reverse=True)
        yield from yield_page_data(filename, headline_menu, all_repo)

    sortkey = "stargazers_count"
    all_repo.sort(key=lambda repo: repo[sortkey], reverse=True)
    user_tags_dict = {d['userdict']['username'].lower(): d['userdict']['tags']
                      for d in db.all() if 'userdict' in d}
    # print(user_tags_dict.keys())
    tag_users_dict = {}
    for username, tags in user_tags_dict.items():
        for tag in tags:
            tag_users_dict.setdefault(tag, []).append(username)
    user_repos_dict = {}
    for repo in all_repo:
        username = repo['username'].lower()
        # print(username)
        user_repos_dict.setdefault(username, []).append(repo)
    for tag, count in tags_info:
        usernames = tag_users_dict[tag]
        tag_repos = []
        for username in usernames:
            tag_repos.extend(user_repos_dict.get(username, []))
            # print(username)
        yield from yield_page_data('location-' + tag, deactivated_headline, tag_repos)
    yield 'locations', '0', deactivated_headline, [], 1, 9999999


def yield_page_data(path, headline_menu, repos):
    chunked_repos_list = chunks(repos, 12)
    max_page_num = len(chunked_repos_list)
    for page_index, chunked_repos in enumerate(chunked_repos_list):
        chunked_repos = [to_tubled_inforow(
            repo) for repo in chunked_repos]
        yield path, page_index + 1, headline_menu, chunked_repos, max_page_num, 30


def to_tubled_inforow(repo):
    """for string,url,do_herf in tubled_inforow"""
    if 'homepage' not in repo:
        print(repo)
        raise
    tubled_inforow = []
    username = repo['username']
    tubled_inforow.append(
        ('name:' + username, "", False))
    tubled_inforow.append(
        ('repo:' + repo['reponame'], repo['html_url'], True))
    tubled_inforow.append(('portfolio website', repo['homepage'], True))
    tubled_inforow.append(
        (f"{repo['stargazers_count']} stars", repo['html_url'] + '/stargazers', True))
    tubled_inforow.append(
        (f"{repo['forks']} forks", repo['html_url'] + '/network/members', True))
    tubled_inforow.append(
        ("updated:" + str(repo['updated_at'])[:10], '', False))
    gif_filename = gen_filename(repo['full_name'])
    location_tags = repo['userdict']['tags'] if 'userdict' in repo else list()
    td = [gif_filename, tubled_inforow, location_tags]
    return td


def iter_headline():
    # {"full_name":"itsdpm\/itsdpm.github.io","html_url":"https:\/\/github.com\/itsdpm\/itsdpm.github.io","description":"Website hosted at -- ","created_at":"2017-12-10T10:48:16Z","updated_at":"2017-12-10T13:39:21Z","size":1,"stargazers_count":0,"watchers_count":0,"forks":0,"watchers":0,"score":4.102341,"gif_success":true}
    for iter_key, url in headline_menus_strings_keys:
        headline_menu = [(url + '0001.html', key, bool(key == iter_key))
                         for key, url in headline_menus_strings_keys]
        yield url, headline_menu


def test_build_static_files():
    paths = ['/a/', '/b/']
    build_static_files(paths)


def test_app():
    import os
    print(app.root_path)
    app.root_path = os.path.join(os.path.dirname(
        app.root_path), 'umihico.github.io')
    print(app.root_path)
    app.run(port=12167)


def put_username():
    for d in db.all():
        username, reponame = d['full_name'].split('/')
        d['username'], d['reponame'] = username, reponame
        db.upsert(d)


if __name__ == "__main__":
    # usernames = load_from_txt('current_users.txt')
    # mention_users_in_issue(usernames)
    # gen_current_users()
    # test_app()
    # test_build_static_files()
    # test_gen_pagenation_bar()
    # put_username()
    render_static_files()
    # css_write()
