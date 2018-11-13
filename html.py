import flask
from common import html_dir, load_db
app = flask.Flask(__name__)


title = 'flask-frozen test'
name1 = 'Taro'
name2 = 'Jiro'


@app.route('/')
def index():
    return flask.render_template(
        'templete.html',
        headline_menu=headline_menu,
        tabulated_repos=tabulated_repos,
    )


@app.route('/test')
def test():
    return flask.render_template('test.html')


if __name__ == "__main__":
    app.run()
