html_dir = "../umihico.github.io/thumbnailed-portfolio-websites/"
from tinydb import TinyDB


def load_db():
    content_tinydb = TinyDB('content_tinydb.json')
    return content_tinydb
