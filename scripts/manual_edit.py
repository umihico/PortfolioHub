from common import db
import tqdm


def add_reponame_username():
    for d in tqdm.tqdm(db.all()):
        if 'reponame' not in d:
            d['username'], d['reponame'] = d['full_name'].split('/')
            db.upsert(d)


if __name__ == '__main__':
    add_reponame_username()
