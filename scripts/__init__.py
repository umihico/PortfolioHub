from download import daily_update
from gen_html import build_static_files
from create_rawdb import create_rawdb

if __name__ == '__main__':
    create_rawdb()
    daily_update()
    build_static_files()
