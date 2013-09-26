from flask import render_template, flash, request, url_for, redirect
from flask.ext.login import login_required, login_user, logout_user

from .router import flask_app
from .auth import setup_login, User

login_manager = setup_login(flask_app)


@login_manager.user_loader
def load_user(username):
    return User(username=username)


@flask_app.route('/')
@login_required
def index():
    return render_template('index.html', debug=False)


@flask_app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        if login_user(User(username), remember=True):
            return redirect(request.args.get("next") or url_for("index"))
        else:
            flash("Sorry, but you could not log in.")
    else:
        flash(u"Invalid username.")
    return render_template("login.html")


@flask_app.route("/logout/")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))
