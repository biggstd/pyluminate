"""
=============
Flask Backend
=============

This module will provide the Flask web application part of Pyluminate.



"""


import flask
import os

app = flask.Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


@app.route('/')
def index():
    greeting = "Pyluminate Index"
    return flask.render_template("index.html", greeting=greeting)


@app.route("/bokeh_demo")
def bokeh_demo():


if __name__ == "__main__":
    app.run()
