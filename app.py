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
SESSION_KEY = 'user_id'


@app.get('/')
def homepage():
    """this redirect to register page"""

    return redirect('/register')


@app.route('/register', methods=["GET", "POST"])
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

        session[SESSION_KEY] = username

        db.session.add(user)
        db.session.commit()

        return redirect(f'/users/{username}')
    else:
        return render_template('register_form.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def handle_login_form():
    """This handles the login form submission"""

    form = LoginForm()

    # Check to see if user already logged in or not and redirect or display
    # based on that.
    if session.get(SESSION_KEY):
        return redirect(f'/users/{session[SESSION_KEY]}')

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            session[SESSION_KEY] = username
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
    if session.get(SESSION_KEY) != username:
        return redirect('/login')
    else:
        user = User.query.filter_by(username=username).one_or_none()
        return render_template('secret.html', user=user, form=form)


@app.post('/logout')
def logout_user():
    """This route removes the logged in user's id from session"""

    form = CSRFOnly()

    if form.validate_on_submit():
        session.pop(SESSION_KEY)
        return redirect('/')


