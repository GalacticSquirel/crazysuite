########################################################################################
######################          Import packages      ###################################
########################################################################################
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from __init__ import db
import re
import requests
import json

auth = Blueprint('auth', __name__) # create a Blueprint object that we name 'auth'

def captcha(form_response):
    with open("secrets.json", "r") as f:
        turnstile_key = (json.loads(f.read()))["cloudflare-turnstile-key"]
    CAPTCHA_url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
    response = (requests.post(CAPTCHA_url, {"secret": turnstile_key, "response": form_response})).json()
    return response["success"]

@auth.route('/login', methods=['GET', 'POST']) # define login page path
def login(): # define login page fucntion
    if request.method=='GET': # if the request is a GET we return the login page
        return render_template('login.html')
    else: # if the request is POST the we check if the user exist and with te right password
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        verify = request.form.get('cf-turnstile-response')
        user = User.query.filter_by(email=email).first()
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user:
            flash('Please sign up before!')
            return redirect(url_for('auth.signup'))
        elif not check_password_hash(user.password, str(password)):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
        # if the above check passes, then we know the user has the right credentials
        if captcha(verify) == True:
            login_user(user, remember=remember)
            return redirect(url_for('main.account'))
        else:
            flash('Failed Captcha!')
            return redirect(url_for("auth.login"))

@auth.route('/signup', methods=['GET', 'POST'])# we define the sign up path
#@login_required
def signup(): # define the sign up function
    if request.method=='GET': # If the request is GET we return the sign up page and forms
        return render_template('signup.html')
    else: # if the request is POST, then we check if the email doesn't already exist and then we save data
        email = str(request.form.get('email'))
        name = request.form.get('name')
        password = request.form.get('password')
        verify = request.form.get('cf-turnstile-response')
        
        errors = []
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not (re.fullmatch(regex, email)):
            flash("Invalid Email")
            return redirect(url_for('auth.signup'))
    
        if name == "" :
            flash("Invalid Name, you must have one")
            return redirect(url_for('auth.signup'))
        if len(list(str(name))) < 4:
            flash("Invalid Name, must be at least 4 characters")
            return redirect(url_for('auth.signup'))
        l, u, p, d = 0, 0, 0, 0
        special = ["!",'"',"#","$","%","&","'","(",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","]","^","_","`","{","|","}","~"]
        s = str(password)
        if s == "":
            flash("Invalid Password, you must have one")
            return redirect(url_for('auth.signup'))
        if (len(s) >= 8):
            for i in s:
                if (i.islower()):
                    l+=1           
                if (i.isupper()):
                    u+=1           
                if (i.isdigit()):
                    d+=1           
                if i in special:
                    p+=1          
        if not (l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(s)):
            
            flash("Invalid Password, include at least one upper and lower letters and one number and a special character")
            return redirect(url_for('auth.signup'))
        
        ip = str(request.remote_addr)


        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        if captcha(verify) == True:
            # create a new user with the form data. Hash the password so the plaintext version isn't saved.
            new_user = User(email=email, name=name, password=generate_password_hash(str(password), method='sha256')) #
            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            flash('Failed Captcha!')
            return redirect(url_for('auth.signup'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/')
def index():
    return render_template("index.html")
