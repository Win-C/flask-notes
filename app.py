""" Notes app that stores passwords hashed with Bcrypt. Yay!"""

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Note
from forms import RegisterForm, LoginForm, AddNoteForm, UpdateNoteForm
from secrets import SECRET_KEY

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///notes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = SECRET_KEY

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route("/")
def homepage_redirect():
    """ Redirect to /register."""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def user_register():
    """ Register user: show form or handle form submission. """

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
    """ Show login form or handle login. """

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
    """ Logs user out and redirects to homepage. """

    session.pop("username", None)
    flash("Logged out!")

    return redirect("/")


##############################################################################
# Logged in user paths

@app.route("/users/<username>")
def user_detail(username):
    """ Show user detail page for logged-in users only. """

    if session.get("username") != username:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        user = User.query.get(username)
        return render_template("user_detail.html", user=user)


@app.route("/users/<username>/delete", methods=["POST"])
def user_delete(username):
    """ Remove the user from the database and also delete all of their notes.
        Clear any user information in the session and redirects. """

    if session.get("username") != username:
        flash("You must be logged in to view!")

    else:
        user = User.query.get(username)
        db.session.delete(user)
        db.session.commit()
        session.pop(username, None)

    return redirect("/")


@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def user_notes_add(username):
    """ Show notes add form or handle note to add."""

    if session.get("username") != username:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        form = AddNoteForm()

        if form.validate_on_submit():
            user = User.query.get(username)

            title = form.title.data
            content = form.content.data
            owner = user.username

            new_note = Note(
                title=title,
                content=content,
                owner=owner,
            )

            db.session.add(new_note)
            db.session.commit()

            return redirect(f"/users/{user.username}")

        else:
            return render_template("user_notes_add.html", form=form)


##############################################################################
# User notes paths


@app.route("/notes/<note_id>/update", methods=["GET", "POST"])
def note_update(note_id):
    """ Show note edit form or handle note update. """

    note = Note.query.get_or_404(note_id)
    username = note.owner

    if session.get("username") != username:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        form = UpdateNoteForm(obj=note)

        if form.validate_on_submit():
            note.title = form.title.data
            note.content = form.content.data

            db.session.commit()

            return redirect(f"/users/{username}")

        else:
            return render_template("note_update.html", form=form, note=note)


@app.route("/notes/<note_id>/delete", methods=["POST"])
def note_delete(note_id):
    """ Delete a note and redirect. """

    note = Note.query.get_or_404(note_id)
    username = note.owner

    if session.get("username") != username:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        db.session.delete(note)
        db.session.commit()

    return redirect(f"/users/{username}")
