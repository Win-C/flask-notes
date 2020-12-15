""" Notes app that stores passwords hashed with Bcrypt. Yay!"""

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///notes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
# TODO: Move secret key to secrets.py
app.config["SECRET_KEY"] = "shhhhhh!"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route("/")
def homepage_redirect():
    """ Redirect to /register."""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def user_register():
    """Register user: produce form & handle form submission."""

    form = RegisterForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_user = User.register(**data)

        db.session.add(new_user)
        db.session.commit()

        session["username"] = new_user.username

        flash(f"{new_user.username} added.")
        # on successful login, redirect to users page
        return redirect(f"/users/{new_user.username}")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def user_login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, password)

        if user:
            session["username"] = user.username  # keep logged in
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("username", None)

    return redirect("/")


################################################################################
# Logged in user paths

@app.route("/users/<username>")
def user_detail(username):
    """Produce user detail page for logged-in users only."""

    if session.get("username") != username:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        user = User.query.get(username)
        return render_template("user_detail.html", user=user)