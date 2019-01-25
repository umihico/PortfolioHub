from flask_frozen import Freezer
from flask import Flask, render_template, redirect
import sys
sys.path.append("..")
from common import htmls_root_dir, jsons_dir, topic
sister_website_name = {
    'personal-website': "thumbnailed-portfolio-websites",
    'portfolio-website': "thumbnailed-personal-websites",
}[topic]
from flask import Markup
from microdb import MicroDB
import collections
import re as re


def chunks(list_, chunk_len):
    '''
    chunks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    >> [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    '''
    return list(list_[i:i + chunk_len] for i in range(0, len(list_), chunk_len))


def numberize(string):
    return int(re.sub(r'\D', '', string))


mdb_repos = MicroDB(jsons_dir+'repos.json', partition_keys=['full_name', ])
print('mdb_repos', len(mdb_repos))
mdb_geotags = MicroDB(jsons_dir+'geotag.json', partition_keys=['username', ])
print('mdb_geotags', len(mdb_geotags))
mdb_gifs = MicroDB(jsons_dir+'gifs.json', partition_keys=['full_name', ])
print('mdb_gifs', len(mdb_gifs))
merged_db = []
for d in mdb_repos.all():
    gif_json = mdb_gifs.get({'full_name': d['full_name']})
    geotag_json = mdb_geotags.get({'username': d['username']}, mdb_geotags.get({
                                  'username': d['username'].lower()}))
    d['gif_path'] = gif_json['filepath']
    if d['gif_path']:
        d['gif_path'] = d['gif_path'].replace(htmls_root_dir, f'/thumbnailed-{topic}s/')
    d['gif_success'] = gif_json['success']
    try:
        d['geotags'] = geotag_json['geotags']
    except Exception as e:
        print(d, geotag_json)
        raise
    d['homepage_exist'] = bool(d['homepage'])
    merged_db.append(d)


app = Flask(__name__)

path_data_dict = {}

headline_menus_strings_keys = [('Most stars', "most_stars"),
                               ('Most forks', "most_forks"), ('Recently updated', "recently_updated"), ]
deactivated_headline = [(url + '0001.html', key, False)
                        for key, url in headline_menus_strings_keys]


def css_write():
    with open('templates/css.css', mode='r') as r:
        with open(htmls_root_dir + 'css.css', mode='w') as w:
            w.write(r.read())


def gen_tags():
    chained_location_tags = []
    for d in merged_db:
        if d['geotags'] and d['gif_success'] and d['homepage_exist']:
            chained_location_tags.extend(d['geotags'])
    counted_tagdict = collections.Counter(chained_location_tags)
    # Counter({'a': 4, 'c': 2, 'b': 1})
    tags_counts = sorted(list(counted_tagdict.items()),
                         key=lambda x: x[1], reverse=True)
    return tags_counts


tags_info = gen_tags()


def render_template_wrapper(headline_menu, repos, pagenation_bar, optional_content=None, tags_num=30):
    return render_template(
        'templete.html',
        topic=topic,
        sister_website_name=sister_website_name,
        tags_info=tags_info,
        tags_num=tags_num,
        headline_menu=headline_menu,
        repos=repos,
        pagenation_bar=pagenation_bar,
        optional_content=optional_content)


@app.route('/<path>/')
def index(path):
    if path == 'favicon.ico':
        return
    if path == 'database.html':
        return alluser()
    if path == 'purpose.html':
        return purpose()
    headline_menu, chunked_repos, max_page_num, tags_num = path_data_dict[path]
    pagenation_bar = gen_pagenation_bar(path, max_page_num)
    return render_template_wrapper(
        headline_menu,
        chunked_repos,
        pagenation_bar,
        tags_num=tags_num
    )


@app.route('/')
def top():
    return redirect('/most_stars0001.html')


def alluser():
    optional_content = []
    optional_content.append([(x, False, x) for x in ['name', 'repository', 'star', 'fork',
                                                     'website', 'valid url', 'gif success', 'pushed_at', 'gif', 'locations']])
    db_sorted_list = sorted(list(merged_db), key=lambda d: (
        d['gif_success'], d['stargazers_count'], d['forks']), reverse=True)
    for d in db_sorted_list:
        full_name = d['full_name']
        repourl = 'https://github.com/' + d['full_name']
        name = d['username']
        star = d['stargazers_count']
        forks = d['forks']
        homepage = d['homepage']
        homepage_exist = d['homepage_exist']
        gif_success = d.get('gif_success', 'not tried')
        pushed_at = d['pushed_at'][:10]
        locations = ','.join(d['geotags'])
        locations = locations if locations else 'None'
        gif_url = d['gif_path']
        tr = []
        for x in [name, repourl, star, forks, homepage,
                  homepage_exist, gif_success, pushed_at, gif_url, locations]:
            value = 'website' if x == homepage else 'gif' if x == gif_url else 'repository' if x == repourl else x
            href_bool = bool(value in ['website', 'gif', 'repository'])
            if x == homepage and x is None:
                href_bool = False
            tr.append((value, href_bool, x))
        optional_content.append(tr)
    for tr in optional_content:
        # print(tr)
        for value, do_href, url in tr:
            pass
    # print(optional_content[0][2][0])
    # optional_content.sort(
    #     key=lambda x: 999999 if x[2][0] == 'star' else x[2][0], reverse=True)

    trs = []
    for tr in optional_content:
        herf_srcs = []
        for value, do_href, url in tr:
            herf_src = f'<a href="{url}">{value}</a>' if do_href else str(
                value)
            herf_srcs.append(herf_src)
        tr_raw_src = '<td nowrap>' + \
            '</td><td nowrap>'.join(herf_srcs) + "</td>"
        trs.append(tr_raw_src)
    trs_raw_src = '<tr>' + '</tr><tr>'.join(trs) + "</tr>"
    raw_src = f'''<table border="1"><h3>if you didn't find yourself, or error with unknown reason, feel free to create issue.</h3>{trs_raw_src}</table>'''
    optional_content = Markup(raw_src)
    return render_template_wrapper(deactivated_headline, list(), list(), optional_content=optional_content)


def purpose():
    purposes = [
        "All websites has brilliant design. Nevertheless only top rated ones get views exponentially, and others get rarely.",
        "learning designs from others takes time if you browse one by one.",
        "It motivate people if they know the rivals in the same region",
        "Or good to find friends too.",
        "Also good for headhunters to filter by region and visit websites directly.",
        "Owners get more visitors as a result.",
        "If you like these ideas, please star this repository."
    ]
    raw_src = "<ul>" + "</ul><ul>".join(purposes) + "</ul>"
    li = '<li style="font-size: 1.3em;">'
    raw_src = li + raw_src + "</li>"
    optional_content = Markup(raw_src)
    return render_template_wrapper(deactivated_headline, list(), list(), optional_content=optional_content)


def gen_pagenation_bar(path, max_page_num):
    if path == 'locations.html':
        return []
    # path="most_stars0001.html"
    current_page = numberize(path)
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


def build_static_files():
    paths = render_static_files()
    freezer = Freezer(app)
    app.config['FREEZER_RELATIVE_URLS'] = False
    app.config['FREEZER_DESTINATION'] = htmls_root_dir
    app.config['FREEZER_DESTINATION_IGNORE'] = ["jsons", "gifs", '.git']

    @freezer.register_generator
    def product_url_generator():
        for path in paths:
            print("writing", path)
            yield "/" + path
    freezer.freeze()
    css_write()


def gen_html_filename(filename, page_index):
    if str(page_index) == '0':
        return filename + '.html'
    else:
        return filename + str(page_index).zfill(4) + '.html'


def iter_page_data():
    """
    *in templete.html*
    for tr_repos in tabulated_repos:
        for filename, tubled_inforows in tr_repost:
            for string,url ,do_herfin tubled_inforow:
    """
    all_repo = merged_db
    all_repo = [
        r for r in all_repo if 'homepage_exist' in r and r['homepage_exist'] and r['gif_success']]
    sortkey_dict = {'most_stars': "stargazers_count",
                    'most_forks': "forks",
                    'recently_updated': "pushed_at", }
    for filename, headline_menu in iter_headline():
        sortkey = sortkey_dict[filename]
        all_repo.sort(key=lambda repo: repo[sortkey], reverse=True)
        yield from yield_page_data(filename, headline_menu, all_repo)

    user_tags_dict = {d['username'].lower(): d['geotags']
                      for d in merged_db if d['geotags']}
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
        tag_repos.sort(
            key=lambda repo: repo['stargazers_count'], reverse=True)
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
        ("updated:" + str(repo['pushed_at'])[:10], '', False))
    gif_filename = repo['gif_path']
    location_tags = repo['geotags']
    td = [gif_filename, tubled_inforow, location_tags]
    return td


def iter_headline():
    # {"full_name":"itsdpm\/itsdpm.github.io","html_url":"https:\/\/github.com\/itsdpm\/itsdpm.github.io","description":"Website hosted at -- ","created_at":"2017-12-10T10:48:16Z","pushed_at":"2017-12-10T13:39:21Z","size":1,"stargazers_count":0,"watchers_count":0,"forks":0,"watchers":0,"score":4.102341,"gif_success":true}
    for iter_key, url in headline_menus_strings_keys:
        headline_menu = [(url + '0001.html', key, bool(key == iter_key))
                         for key, url in headline_menus_strings_keys]
        yield url, headline_menu


def render_static_files():
    for filename, page_index, headline_menu, chunked_repos, max_page_num, tags_num in iter_page_data():
        print("calculating", filename, page_index)
        path_data_dict[gen_html_filename(filename, page_index)] = (
            headline_menu, chunked_repos, max_page_num, tags_num)
    paths = list(path_data_dict.keys())
    paths.append('database.html')
    paths.append('purpose.html')
    return paths


if __name__ == "__main__":
    build_static_files()
