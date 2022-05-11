from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meh.db'

class regiration_form (FlaskForm):
    username = StringField(validators=[
        InputRequired(),
        Length (min = 4, max=20)
    ], render_kw= {"placeholder":"username"})
    password= PasswordField(validators=[
        InputRequired(),
        Length (min = 4, max=20)
    ], render_kw= {"placeholder":"password"})
    submit = SubmitField("register")


class User(db.Model, UserMixin):
    """Model for user accounts."""
    __tablename__ = 'users'
    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String,
                         nullable=False,
                         unique=True)
    email = db.Column(db.String(40),
                      unique=True,
                      nullable=True)
    password = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)
    def __repr__(self):
        return '<User {}>'.format(self.username)


if __name__ == "__main__":
    app.run(debug=True)
