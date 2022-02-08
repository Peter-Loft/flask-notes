""" Flask App for Notes App"""

from forms import RegisterForm
from flask import Flask, render_template, redirect
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

        user = User(username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name)

        db.session.add(user)
        db.session.commit()

        return redirect('/secret')
    else:
        return render_template('register_form.html', form=form)