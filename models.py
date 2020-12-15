from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        primary_key=True
        )

    password = db.Column(
        db.Text,
        nullable=False,
        )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
        )

    first_name = db.Column(
        db.String(30),
        nullable=False,
        )

    last_name = db.Column(
        db.String(30),
        nullable=False,
        )

    def __repr__(self):

        return f"<User {self.username}, {self.first_name}, {self.last_name}>"

    # start_register
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """ Register user w/hashed password, email, first name and last name
            return user. """

        # TODO: play with workfactor setting later
        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        # return instance of user w/username and hashed pwd
        return cls(
            username=username,
            password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name,
            )

    # end_register
