import os

from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import CSRFProtectForm, RegisterUserForm, LoginUserForm

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
    user = User.query.get_or_404(username)

    if session.get("username") == username:
        return render_template("user.html", user=user, form=form)
    else:
        return redirect('/login')


@app.post('/logout')
def logout_user():
    """logs out user from session"""

    session.pop("username", None)

    return redirect('/login')
