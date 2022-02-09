""" Flask App for Notes App"""


from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
from forms import RegisterForm, LoginForm, CSRFOnly

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///notes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "some$tring"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.get('/')
def homepage():
    """this redirect to register page"""

    return redirect('/register')

# CR: consider combining GET/POST for same routes


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

        session["user_id"] = username

        db.session.add(user)
        db.session.commit()

        return redirect(f'/users/{username}')
    else:
        return render_template('register_form.html', form=form)

# CR: Check to see if user already logged in or not and redirect or display
# based on that.


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
            # CR: set "user_id" string to a global variable to be safer
            session["user_id"] = username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login_form.html", form=form)


@app.get('/users/<username>')
def user_detailed_page(username):
    """this display user detailed page"""

    # check session to make sure current user is authenticated
    form = CSRFOnly()

    # CR: Refactor for 'failfast' framing
    if session['user_id'] == username:
        user = User.query.filter_by(username=username).one_or_none()

        return render_template('secret.html', user=user, form=form)
    else:
        return redirect('/login')


@app.post('/logout')
def logout_user():
    """This route removes the logged in user's id from session"""
    form = CSRFOnly()

    if form.validate_on_submit():
        session.pop('user_id')
        return redirect('/')
    else:
        return redirect('/secret')