from common import database_dir, DictTinyDB
from dbs import rawdb, db, ldb
import tqdm
import time


def tinydb2microdb():
    from microdb import MicroDB
    import os
    for filename, key in [('location.json', 'username'), ('rawdb.json', 'html_url'), ('db.json', 'html_url')]:
        fullpath = database_dir + filename
        xdb = DictTinyDB(fullpath, key)
        dicts = list(xdb.all())
        os.remove(fullpath)
        mdb = MicroDB(fullpath, (key,))
        for d in dicts:
            mdb.upsert(d)
        mdb.save()


def manual_edit():
    for d in tqdm.tqdm(db.all()):
        d['last_found_date'] = int(time.time())
        db.upsert(d)
        # if 'reponame' not in d:
        #     d['username'], d['reponame'] = d['full_name'].split('/')
        #     db.upsert(d)


if __name__ == '__main__':
    tinydb2microdb()
