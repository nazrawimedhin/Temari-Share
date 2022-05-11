from crypt import methods
from click import password_option
from flask import Flask, flash, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required, login_user, LoginManager, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from flask_bcrypt import Bcrypt

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "0035b8a299c4d41650db"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class regiration_form (FlaskForm):
    """this will create registration form for user

    Args:
        FlaskForm (form formatter): create dorm 

    Raises:
        ValidationError: check if there is any oter user with the same user name
    """
    username = StringField(validators=[
        InputRequired(),
        Length(min=4, max=20)
    ], render_kw={"placeholder": "username"})
    full_name = StringField(validators=[
        InputRequired(),
        Length(min=4, max=20)
    ], render_kw={"placeholder": "Full name"})
    password = PasswordField(validators=[
        InputRequired(),
        Length(min=4, max=20)
    ], render_kw={"placeholder": "password"})

    confirm_password = PasswordField(validators=[
        InputRequired(),
        EqualTo("password")
    ], render_kw={"placeholder": "confirm password"})

    submit = SubmitField("register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'the usernae already exist....'
            )
    # def validate_password(self, password):
    #     if password.data() != self.confirm_password.data ():
    #         raise ValidationError(
    #             'the not matched passwords ....'
    #         )


class Login_from (FlaskForm):
    """tis is login form that will applly on login page

    Args:
        FlaskForm (class): 
    """
    username = StringField(validators=[
        InputRequired(),
        Length(min=4, max=20)
    ], render_kw={"placeholder": "username"})
    password = PasswordField(validators=[
        InputRequired(),
        Length(min=4, max=20)
    ], render_kw={"placeholder": "password"})
    submit = SubmitField("login")


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    full_name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)


@app.route('/')
def home():
    """this is home just for trying

    Returns:
        html: home page just status
    """
    return render_template('home.html')


@app.route("/dashbord", methods=['GET', 'POST'])
@login_required
def dashbord():
    return render_template("dashbrd.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    """this is a route for login page

    Returns:
        login.html in tempate: so the form can be here
    """

    form = Login_from()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("dashbord"))
            else:
                return render_template('login.html', form=form, password_error="check your password")
        else:
            return render_template('try.html', form=form, user_error="user dons't exist")
    return render_template('login.html', form=form)


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=['GET', 'POST'])
def register():
    """this is a rigstration route 

    Returns:
        registration form : tobe filled
    """
    form = regiration_form()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,
                        password=hashed_password, full_name=form.full_name.data)
        db.session.add(new_user)
        db.session.commit()
        flash(
            f'account created!!!  for pls login with ur new account {new_user.username}')
        return redirect(url_for("login"))
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
