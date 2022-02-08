""" Flask App for Notes App"""

from forms import RegisterForm, LoginForm
from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///notes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.get('/')
def homepage():
    """this redirect to register page"""

    return redirect('/register')


@app.get('/register')
def show_register_form():
    """this show register form to user"""

    form = RegisterForm()

    return render_template('register_form.html', form=form)


@app.post('/register')
def handle_register_form():
    """this process the register form for new user"""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(
            username, password, email, first_name, last_name)

        session["user_id"] = user.username

        db.session.add(user)
        db.session.commit()

        return redirect('/secret')
    else:
        return render_template('register_form.html', form=form)


@app.get('/login')
def show_login_form():
    """This renders the login_form.html template"""

    form = LoginForm()

    return render_template('login_form.html', form=form)


@app.post('/login')
def handle_login_form():
    """This handles the login form submission"""

    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["user_id"] = username
            return redirect('/secret', user=user)
        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login_form.html", form=form)
