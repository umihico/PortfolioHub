from dbs import rawdb, db, ldb
import tqdm
import time


def manual_edit():
    for d in tqdm.tqdm(db.all()):
        del d['last_found_date']
        db.upsert(d)
    db.save()
    # if 'reponame' not in d:
    #     d['username'], d['reponame'] = d['full_name'].split('/')
    #     db.upsert(d)


if __name__ == '__main__':
    manual_edit()
