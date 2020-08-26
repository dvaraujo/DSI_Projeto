from flask import request, render_template, redirect, url_for
from flask import current_app as app


@app.route("/")
def index():
    return "<h1> Deu certo </h1>"


