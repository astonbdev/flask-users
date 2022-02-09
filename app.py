import os

from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Note
from forms import CSRFProtectForm, RegisterUserForm, LoginUserForm, NoteForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///hashing_login"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ["API_SECRET_KEY"]

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.get('/')
def show_homepage():
    """displays homepage"""

    return redirect('/register')


@app.route('/register', methods=["GET", "POST"])
def register_new_user():
    """adds user to db after validating then logs user into session"""

    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(
            username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()

        session['username'] = new_user.username

        return redirect(f'/users/{username}')

    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login_user():
    """log user into session"""

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(f'/users/{username}')

        else:
            form.username.errors = ['Bad name/password']

    return render_template('login.html', form=form)


@app.get('/users/<username>')
def show_user(username):
    """displays user information"""

    form = CSRFProtectForm()
    noteCSRFForm = CSRFProtectForm()
    user = User.query.get_or_404(username)

    if session.get("username") == username:
        return render_template(
            "user.html",
            user=user,
            form=form,
            noteCSRF=noteCSRFForm)
    else:
        return redirect('/login')


@app.post('/logout')
def logout_user():
    """logs out user from session"""

    session.pop("username", None)

    return redirect('/login')


@app.route('/users/<username>/notes/add', methods=["GET", "POST"])
def add_user_note(username):
    """Add notes to the user if the data is valid and redirect to user detail
    page, or it still show the add note form
    """
    form = NoteForm()

    user = User.query.get_or_404(username)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(title=title, content=content)

        user.notes.append(note)

        db.session.commit()

        return redirect(f'/users/{username}')

    return render_template("add_note.html", username=user.username, form=form)


@app.route('/notes/<int:note_id>/update', methods=["GET", "POST"])
def update_user_note(note_id):
    """update user note and after click the update button, redirect to user
    page
    """
    note = Note.query.get_or_404(note_id)

    form = NoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        return redirect(f'/users/{note.owner}')

    return render_template("update_note.html", form=form, note=note)


@app.post('/notes/<int:note_id>/delete')
def delete_note(note_id):
    """delete the note of given note id, and redirect to user page"""
    note = Note.query.get_or_404(note_id)
    username = note.owner
    db.session.delete(note)
    db.session.commit()
    return redirect(f'/users/{username}')


@app.post('/users/<username>/delete')
def delete_user(username):
    """delete the user and the user notes, and remove the user from the session,
    redirect to homepage"""
    user = User.query.get_or_404(username)

    if user.notes:
        Note.query.filter(Note.owner == username).delete()
        # db.session.delete(notes)
        db.session.delete(user)
    else:
        db.session.delete(user)

    db.session.commit()

    session.pop("username", None)

    return redirect('/')
