from microdb import MicroDB
database_dir = '../database/'
ldb = MicroDB(database_dir + 'location.json', ['username', ])
rawdb = MicroDB(database_dir + 'rawdb.json', ['html_url', ])
db = MicroDB(database_dir + 'db.json', ['html_url'])
