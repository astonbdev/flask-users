from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User class"""

    __tablename__ = "users"

    username = db.Column(db.String(20),
                         primary_key=True,
                         nullable=False,
                         unique=True)

    password = db.Column(db.String(100),
                         nullable=False)

    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)

    first_name = db.Column(db.String(30),
                           nullable=False)

    last_name = db.Column(db.String(30),
                          nullable=False)

    

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Creates user instance, hashes password"""

        hashed_pwd = bcrypt.generate_password_hash(pwd).decode("utf8")

        user = cls(
            username=username,
            password=hashed_pwd,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        return user

    @classmethod
    def authenticate(cls, username, pwd):
        """authenticate user"""

        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False


class Note(db.Model):
    """Note class"""

    __tablename__ = "notes"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)

    owner = db.Column(db.Text,
                      db.ForeignKey("users.username"))

    user = db.relationship("User", backref="notes")