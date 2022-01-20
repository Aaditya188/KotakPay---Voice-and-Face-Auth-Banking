from flask import Flask, render_template, request, url_for, redirect, Blueprint, send_from_directory
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
import os
from login import login_check as lc
from register import register_on_submit as rs

main = Blueprint('main', __name__)

secret_key = str(os.urandom(24))

app = Flask(__name__)
app.config['TESTING'] = False
app.config['DEBUG'] = True
app.config['FLASK_ENV'] = 'deployment'
app.config['SECRET_KEY'] = secret_key

app.register_blueprint(main)

class LoginForm(FlaskForm):
    email = PasswordField('Transaction Password', validators=[DataRequired()])
    url = StringField('DataURL', validators=[])
    submit = SubmitField('LOGIN')

email = None
url = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global email, url
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        url = form.url.data
        return redirect(url_for('.login'))
    elif request.method == 'POST':
        form.email.data = email
        form.url.data = url
    return render_template('index.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    global email, url
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        url = form.url.data
        return redirect(url_for('.register_submit'))
    elif request.method == 'POST':
        form.email.data = email
        form.url.data = url
    return render_template('register.html', form=form)

@app.route('/login')
def login():
    global email, url
    if email == '' or url == '':
        return redirect(url_for('.index'))
    if email == None or url == None:
        return redirect(url_for('.login'))
    status = lc(email, url)
    if status == "Image not clear! Please try again!":
        return render_template('fail.html', greet="Oops! Not Failed to Login", st= "Image Not Clear")
    if status == "Data does not exist!":
        return render_template('fail.html', greet="Oops! Not Failed to Login", st= "Data Not Exist")
    if status == "Successfully Logged in!":
        app.logger.info("Login Success")
        return render_template('success.html', greet="Congrats! You are Logged in to Kotak Pay", st= "Face Verified")
    else:
        app.logger.info("Login Fail")
        return render_template('fail.html', greet="Oops! Not Able to Log In", st= "Login Failed")

@app.route('/register_submit')
def register_submit():
    global email, url
    if email == '' or url == '':
        return redirect(url_for('.register'))
    if email == None or url == None:
        return redirect(url_for('.register_submit'))
    status = rs(email, url)
    if status == "Registration Successful!":
        app.logger.info("Registration Success")
        return render_template('success.html', greet="Congrats! You are Registered for Kotak Pay", st= "Registration Success")
    else:
        app.logger.info("Registration fail")
        return render_template('fail.html', greet="Oops! Not Able to Register", st= "Registration Failed")

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(port=9999)