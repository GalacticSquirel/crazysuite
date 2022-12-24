
import json
import json
import os
import re

from flask import (
    Blueprint,
    flash,
    flash,
    jsonify,
    redirect,
    redirect,
    render_template,
    render_template,
    request,
    request,
    send_file,
    url_for,
    url_for,
)
from flask_limiter import Limiter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.util import get_remote_address
from flask_login import current_user, login_required
from flask_login import current_user, login_required, login_user, logout_user
from git.cmd import Git
from git.repo import Repo
import requests
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from __init__ import create_app, db
from models import User

main = create_app()
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(main)


@main.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        os.system("git reset --hard HEAD")
        repopull = Git().pull('https://github.com/GalacticSquirel/crazysuite.git')

        return jsonify({"message": str(repopull)})
    else:
        return jsonify({"error": "Failed"})


@main.route('/')
def index():
    return redirect('/home')


@main.route('/home')
def home():
    return render_template('index.html')


@main.route('/favicon.ico')
def favicon():
    return send_file('templates//favicon.ico', mimetype='image/gif')


@main.route('/account')
@login_required
def account():
    return render_template('account.html', name=current_user.name)


@main.route('/shop')
def shop():
    shop_items = json.load(open('static/items.json', 'r'))
    with_urls = list(shop_items)
    return render_template('shop.html', shop_items=with_urls)

@main.route('/shop/productdetails.css')
def product_detailscss():
    return send_file('templates//productdetails.css')


@main.route('/shop/style.css')
def product_detailsstylecss():
    return send_file('templates//style.css')


@main.route('/signup.css')
def signupcss():
    return send_file('templates//signup.css')



@main.route('/login.css')
def logincss():
    return send_file('templates//login.css')



@main.route('/admin.css')
def consolecss():
    return send_file('templates//console.css')


@main.route('/style.css')
def stylecss():
    return send_file('templates//style.css')


@main.route('/account.css')
def accountcss():
    return send_file('templates//account.css')


@main.route('/home.css')
def homecss():
    return send_file('templates//index.css')


@main.route('/not_found.css')
def errornot_foundcss():
    return send_file('templates//not_found.css')


@main.route('/shop.css')
def shopcss():
    return send_file('templates//shop.css')


@main.route('/terms')
def terms():
    return render_template('terms.html')


@main.route('/terms.css')
def termscss():
    return send_file('templates//terms.css')


@main.route('/About-Us')
def about_us():
    return render_template('about-us.html')


@main.route('/terms.css')
def about_uscss():
    return send_file('templates//about-us.css')


@main.route('/rate-limit.css')
def rate_limitcss():
    return send_file('templates//rate_limit.css')

@main.route('/images/<image_name>')
def images(image_name):
    if str(image_name) + ".png" in os.listdir("templates//images"):
        return send_file(f"templates//images//{image_name}.png")
    else:
        return send_file(f"templates//images//place_holder.png")


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return True if filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS else False

@main.route('/shop/<string:item_name>')
def productdetails(item_name):
    addresses = []
    shop_items = json.load(open('static/items.json', 'r'))
    for item in shop_items:
        addresses.append(item["page_name"])

    try:
        index = addresses.index(item_name)
    except ValueError:
        item_details = {"name": "Name",
                        "page_name": "",
                        "description": "",
                        "full_description": "Description",
                        "genre": "Genre",
                        "image_url": "/images/place_holder",
                        "price": "Price",
                        "big_image_url": "/images/place_holder"}
        return render_template("productdetails.html", item_details=item_details)
    item_details = {"name": shop_items[index]["name"],
                    "page_name": shop_items[index]["page_name"],
                    "description": shop_items[index]["description"],
                    "full_description": shop_items[index]["full_description"],
                    "genre": shop_items[index]["genre"],
                    "image_url": shop_items[index]["image_url"],
                    "price": shop_items[index]["price"],
                    "big_image_url": shop_items[index]["big_image_url"]}
    return render_template('productdetails.html', item_details=item_details)


@main.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.id in [1, 2]:
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']

            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if allowed_file(file.filename):
                file.save(f"templates/images/{file.filename}")
            return redirect(url_for('main.admin'))
        return render_template('console.html')
    else:
        return redirect('/')


@main.route('/admin/add', methods=['GET', 'POST'])
@login_required
def add():
    if current_user.id in [1, 2]:
        form = request.form
        info = {"name": form.get("name"), "page_name": form.get("page_name"), "description": form.get(
            "description"), "full_description": form.get("full_description"), "price": form.get("price"), "genre": form.get("genre")}
        # info = list(map(lambda x: form.get(x), info_names))
        info["image_url"] = (
            url_for('main.images', image_name=form.get("image_name")))
        info["big_image_url"] = (
            url_for('main.images', image_name=form.get("big_image_name")))

        with open('static/items.json', 'r') as f:
            curr_items = json.load(f)

        curr_items.append(info)
        with open('static/items.json', 'w') as f:
            json.dump(curr_items, f)
        return redirect(url_for('main.admin'))
    else:
        return redirect('/')


@main.route("/api/prices")
@limiter.limit("48/day")
@limiter.limit("2/hour")
def api_prices():
    with open("static//items.json", "rb") as f:
        items = json.load(f)
    prices = dict()
    for item in items:
        prices[item["name"]] = item["price"]
    with open("static//prices.json", "w") as f:
        json.dump(prices, f)
    return send_file("static//prices.json")


def captcha(form_response):
    with open("secrets.json", "r") as f:
        turnstile_key = (json.loads(f.read()))["cloudflare-turnstile-key"]
    CAPTCHA_url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
    response = (requests.post(
        CAPTCHA_url, {"secret": turnstile_key, "response": form_response})).json()
    return response["success"]


@main.route('/login', methods=['GET', 'POST'])  # define login page path
@limiter.limit("24/day")
@limiter.limit("30/hour")
@limiter.limit("30/minute")
@limiter.limit("1/second")
def login():  # define login page fucntion
    if not current_user.is_authenticated:
        if request.method == 'GET':  # if the request is a GET we return the login page
            return render_template('login.html')
        else:  # if the request is POST the we check if the user exist and with te right password
            email = request.form.get('email')
            password = request.form.get('password')
            remember = True if request.form.get('remember') else False
            verify = request.form.get('cf-turnstile-response')
            user = User.query.filter_by(email=email).first()
            # check if the user actually exists
            # take the user-supplied password, hash it, and compare it to the hashed password in the database
            if not user:
                flash('Please sign up before!')
                return redirect(url_for('main.signup'))
            elif not check_password_hash(user.password, str(password)):
                flash('Please check your login details and try again.')
                # if the user doesn't exist or password is wrong, reload the page
                return redirect(url_for('main.login'))
            # if the above check passes, then we know the user has the right credentials
            if captcha(verify) == True:
                login_user(user, remember=remember)
                return redirect(url_for('main.account'))
            else:
                flash('Failed Captcha!')
                return redirect(url_for("main.login"))
    else:
        return redirect('/')


@main.route('/signup', methods=['GET', 'POST'])  # we define the sign up path
@limiter.limit("1/day")
# @login_required
def signup():  # define the sign up function
    if not current_user.is_authenticated:
        if request.method == 'GET':  # If the request is GET we return the sign up page and forms
            return render_template('signup.html')
        else:  # if the request is POST, then we check if the email doesn't already exist and then we save data
            email = str(request.form.get('email'))
            name = request.form.get('name')
            password = request.form.get('password')
            verify = request.form.get('cf-turnstile-response')

            errors = []
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if not (re.fullmatch(regex, email)):
                flash("Invalid Email")
                return redirect(url_for('main.signup'))

            if name == "":
                flash("Invalid Name, you must have one")
                return redirect(url_for('main.signup'))
            if len(list(str(name))) < 4:
                flash("Invalid Name, must be at least 4 characters")
                return redirect(url_for('main.signup'))
            l, u, p, d = 0, 0, 0, 0
            special = ["!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/",
                       ":", ";", "<", "=", ">", "?", "@", "[", "]", "^", "_", "`", "{", "|", "}", "~"]
            s = str(password)
            if s == "":
                flash("Invalid Password, you must have one")
                return redirect(url_for('main.signup'))
            if (len(s) >= 8):
                for i in s:
                    if (i.islower()):
                        l += 1
                    if (i.isupper()):
                        u += 1
                    if (i.isdigit()):
                        d += 1
                    if i in special:
                        p += 1
            if not (l >= 1 and u >= 1 and p >= 1 and d >= 1 and l+p+u+d == len(s)):

                flash(
                    "Invalid Password, include at least one upper and lower letters and one number and a special character")
                return redirect(url_for('main.signup'))

            ip = str(request.remote_addr)

            # if this returns a user, then the email already exists in database
            user = User.query.filter_by(email=email).first()
            if user:  # if a user is found, we want to redirect back to signup page so user can try again
                flash('Email address already exists')
                return redirect(url_for('main.signup'))

            if captcha(verify) == True:
                # create a new user with the form data. Hash the password so the plaintext version isn't saved.
                new_user = User(email=email, name=name, password=generate_password_hash(
                    str(password), method='sha256'))
                # add the new user to the database
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('main.login'))
            else:
                flash('Failed Captcha!')
                return redirect(url_for('main.signup'))
    else:
        return redirect('/')


@main.route('/ChangePass', methods=['POST'])
@limiter.limit("12/day")
@limiter.limit("1/hour")
@login_required
def ChangePass():
    email = str(request.form.get('email'))
    old_password = str(request.form.get('old-password'))
    new_password = str(request.form.get('new-password'))
    verify = request.form.get('cf-turnstile-response')

    errors = []
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not (re.fullmatch(regex, email)):  # check valid email
        return redirect('/account')
    l, u, p, d = 0, 0, 0, 0
    special = ["!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/",
               ":", ";", "<", "=", ">", "?", "@", "[", "]", "^", "_", "`", "{", "|", "}", "~"]
    s = str(new_password)
    if s == "":
        return redirect('/account')
    if (len(s) >= 8):
        for i in s:
            if (i.islower()):
                l += 1
            if (i.isupper()):
                u += 1
            if (i.isdigit()):
                d += 1
            if i in special:
                p += 1
    if not (l >= 1 and u >= 1 and p >= 1 and d >= 1 and l+p+u+d == len(s)):  # check new password valid
        return redirect('/account')

    ip = str(request.remote_addr)

    if old_password == new_password:  # check both passwords entered are the same
        return redirect('/account')

    user = User.query.filter_by(email=email).first()
    if not user:
        return redirect('/account')

    if not check_password_hash(user.password, str(old_password)):
        return redirect('/account')

    if captcha(verify) == True:
        current_user.password = generate_password_hash(
            str(new_password), method='sha256')
        db.session.commit()
        return redirect('/account')
    else:
        return redirect('/account')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

def handle_not_found(error):
    return render_template('not_found.html'), 404


def rate_limit_reached(error):
    return render_template('rate_limit.html'), 429


if __name__ == '__main__':
    db.create_all(app=create_app())
    main.register_error_handler(429, rate_limit_reached)
    main.register_error_handler(404, handle_not_found)
    main.run(debug=True, host='0.0.0.0')


# profile page is controls
