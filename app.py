import os

from flask import Flask, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegisterUserForm

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

    return redirect('/register')


@app.route('/register', methods=["GET", "POST"])
def register_new_user():
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

        return redirect('/secret')

    else:
        return render_template('register.html', form=form)
