
import json
import os
import re

from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import current_user, login_required, login_user, logout_user
from git.cmd import Git
from git.repo import Repo
import requests
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from __init__ import create_app, db
from models import User
import key_management as keys

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

########################################################################
########################################################################
#######################       Endpoints        #########################
########################################################################
########################################################################
@main.route('/')
@limiter.limit("1/second")
def index():
    return redirect('/home')


@main.route('/home')
@limiter.limit("1/second")
def home():
    return render_template('index.html')


@main.route('/favicon.ico')
def favicon():
    return send_file('templates//favicon.ico', mimetype='image/gif')


@main.route('/account')
@limiter.limit("1/second")
@login_required
def account():
    return render_template('account.html', name=current_user.name)


@main.route('/shop')
@limiter.limit("1/second")
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
@limiter.limit("1/second")
def terms():
    return render_template('terms.html')


@main.route('/terms.css')
def termscss():
    return send_file('templates//terms.css')


@main.route('/About-Us')
@limiter.limit("1/second")
def about_us():
    return render_template('about-us.html')


@main.route('/terms.css')
def about_uscss():
    return send_file('templates//about-us.css')


@main.route('/rate-limit.css')
def rate_limitcss():
    return send_file('templates//rate_limit.css')


@main.route('/shop/<string:item_name>')
@limiter.limit("1/second")
def productdetails(item_name: str):
    """
        Render the product details page for the given item. If the item does not exist, render a placeholder page.

        Args:
        item_name: The name of the item to display the details for.

        Returns:
        Render: The product details page for the given item, or a placeholder page if the item does not exist.
    """
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

########################################################################
########################################################################
#######################       Logic        #############################
########################################################################
########################################################################


def allowed_file(filename: str) -> bool:
    """
    Check if a given file has an allowed file extension.

    Args:
    filename: The name of the file to check.

    Returns:
    bool: True if the file has an allowed extension, False otherwise.
    """
    return True if filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'} else False


def password_check(password: str) -> bool:
    l, u, p, d = 0, 0, 0, 0
    special = ["!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/",
               ":", ";", "<", "=", ">", "?", "@", "[", "]", "^", "_", "`", "{", "|", "}", "~"]
    s = str(password)
    if s == "":
        return False
    if s == None:
        return False
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
        return False
    return True


########################################################################
########################################################################
#######################       Admin        #############################
########################################################################
########################################################################


@main.route('/images/<image_name>')
def images(image_name: str):
    """
    Send the requested image file if it exists, otherwise send a placeholder image.

    Args:
    image_name: The name of the requested image file.

    Returns:
    Send file: The requested image file if it exists, otherwise the placeholder image file.
    """
    if str(image_name) + ".png" in os.listdir("templates//images"):
        return send_file(f"templates//images//{image_name}.png")
    else:
        return send_file(f"templates//images//place_holder.png")


@main.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    """
        Render the admin console page, or redirect the user if they do not have permission. If a file is submitted through the form, save it if it has an allowed file extension.

        Args:
        None

        Returns:
        Render: The admin console page if the user has permission, a redirect to the home page if the user does not have permission.
    """
    if current_user.id in [1, 2]:
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']

            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if not file.filename == None:
                if allowed_file(file.filename):
                    file.save(f"templates/images/{file.filename}")
                return redirect(url_for('admin'))
        return render_template('console.html')
    else:
        return redirect('/')


@main.route('/admin/add', methods=['GET', 'POST'])
@login_required
def add():
    """
        Add a new product to the shop item list if the current user has permission.

        Args:
        None

        Returns:
        Render: A redirect to the admin console page if the user has permission, a redirect to the home page if the user does not have permission.
    """
    if current_user.id in [1, 2]:
        form = request.form
        info = {"name": form.get("name"), "page_name": form.get("page_name"), "description": form.get(
            "description"), "full_description": form.get("full_description"), "price": form.get("price"), "genre": form.get("genre")}
        info["image_url"] = (
            url_for('images', image_name=form.get("image_name")))
        info["big_image_url"] = (
            url_for('images', image_name=form.get("big_image_name")))

        with open('static/items.json', 'r') as f:
            curr_items = json.load(f)

        curr_items.append(info)
        with open('static/items.json', 'w') as f:
            json.dump(curr_items, f)
        return redirect(url_for('admin'))
    else:
        return redirect('/')

########################################################################
########################################################################
#######################       API        ###############################
########################################################################
########################################################################


@main.route("/api/prices")
@limiter.limit("48/day")
@limiter.limit("2/hour")
def api_prices():
    with open("static//items.json", "rb") as f:
        items = json.load(f)
    prices = list(map(lambda product: product['name'], items))
    with open("static//prices.json", "w") as f:
        json.dump(prices, f)
    return send_file("static//prices.json")


########################################################################
########################################################################
#######################       Auth       ###############################
########################################################################
########################################################################
def captcha(form_response: str) -> bool:
    """
        Check the validity of the provided CAPTCHA response.

        Args:
        form_response (str): The CAPTCHA response provided by the user.

        Returns:
        bool: True if the CAPTCHA response is valid, False otherwise.
    """
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
def login():
    """
        Handle the login process for a user.

        Verify the provided email and password against the database. If the user exists and the password is correct, log the user in and redirect them to their account page. If the user does not exist or the password is incorrect, display an error message and redirect the user back to the login page. If the request is a GET request, display the login page.

        Args:
        email (str): The email address provided by the user.
        password (str): The password provided by the user.
        remember (bool): A flag indicating whether the user's login should be remembered.
        verify (str): The CAPTCHA response provided by the user.

        Returns:
        Render: The function redirects the user to the appropriate page.
    """
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
                return redirect(url_for('signup'))
            elif not check_password_hash(user.password, str(password)):
                flash('Please check your login details and try again.')
                # if the user doesn't exist or password is wrong, reload the page
                return redirect(url_for('login'))
            # if the above check passes, then we know the user has the right credentials
            if verify == None:
                flash('Failed Captcha!')
                return redirect(url_for("login"))
            if captcha(verify) == True:
                login_user(user, remember=remember)
                return redirect(url_for('account'))
            else:
                flash('Failed Captcha!')
                return redirect(url_for("login"))
    else:
        return redirect('/')


@main.route('/signup', methods=['GET'])  # we define the sign up path
@limiter.limit("30/minute")
@limiter.limit("1/second")
def signup():  # define the sign up function
    if not current_user.is_authenticated:
        return render_template('signup.html')
    else:
        return redirect('/')


@main.route('/signup', methods=['POST'])  # we define the sign up path
@limiter.limit("15/minute")
@limiter.limit("1/second")
# @login_required
def signupPOST():  # define the sign up function
    """
        Handles the sign up process for a new user.
        Validates the user's input for the email, name, and password.
        If the input is valid, a new user is created in the database with a hashed password.
        If the input is invalid, an error message is displayed and the user is redirected to the sign up page.
    """
    if not current_user.is_authenticated:
        email = str(request.form.get('email'))
        name = request.form.get('name')
        password = request.form.get('password')
        verify = request.form.get('cf-turnstile-response')

        errors = []
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not (re.fullmatch(regex, email)):
            flash("Invalid Email")
            return redirect(url_for('signup'))

        if name == "":
            flash("Invalid Name, you must have one")
            return redirect(url_for('signup'))
        if len(list(str(name))) < 4:
            flash("Invalid Name, must be at least 4 characters")
            return redirect(url_for('signup'))

        if not password_check(str(password)):
            flash("Invalid Password, include at least one upper and lower letters and one number and a special character")
            return redirect(url_for('signup'))

        # if this returns a user, then the email already exists in database
        user = User.query.filter_by(email=email).first()
        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('signup'))
        if verify == None:
            flash('Failed Captcha!')
            return redirect(url_for("login"))
        if captcha(verify) == True:
            # create a new user with the form data. Hash the password so the plaintext version isn't saved.
            new_user = User(email=email, name=name, password=generate_password_hash(
                str(password), method='sha256'))
            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            flash('Failed Captcha!')
            return redirect(url_for('signup'))
    else:
        return redirect('/')


@main.route('/ChangePass', methods=['POST'])
@limiter.limit("12/day")
@limiter.limit("1/hour")
@login_required
def ChangePass():
    """
        Handle the password change process for a user.

        Validate the provided email, old password, and new password for the user. If the input is valid, change the user's password in the database. If the input is invalid, redirect the user back to their account page.

        Args:
        email (str): The email address provided by the user.
        old_password (str): The user's current password.
        new_password (str): The user's desired new password.
        verify (str): The CAPTCHA response provided by the user.

        Returns:
        None: The function redirects the user to the appropriate page.
    """
    email = str(current_user.email)
    old_password = str(request.form.get('old-password'))
    new_password = str(request.form.get('new-password'))
    verify = request.form.get('cf-turnstile-response')

    errors = []  # TODO: implement multiple error catching so that all errors can be displayed
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not (re.fullmatch(regex, email)):
        return redirect('/account')
    if not password_check(str(new_password)):
        return redirect('/account')

    ip = str(request.remote_addr)

    if old_password == new_password:  # check both passwords entered are the same
        return redirect('/account')

    user = User.query.filter_by(email=email).first()
    if not user:
        return redirect('/account')

    if not check_password_hash(user.password, str(old_password)):
        return redirect('/account')
    if verify == None:
        flash('Failed Captcha!')
        return redirect(url_for("login"))
    if captcha(verify) == True:
        current_user.password = generate_password_hash(
            str(new_password), method='sha256')
        db.session.commit()
        return redirect('/account')
    else:
        return redirect('/account')


@main.route('/logout')
@limiter.limit("1/second")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

########################################################################
########################################################################
#######################       Errors        ############################
########################################################################
########################################################################


def handle_not_found(error):
    return render_template('not_found.html'), 404


def rate_limit_reached(error):
    return render_template('rate_limit.html'), 429


if __name__ == '__main__':
    db.create_all(app=create_app())
    main.register_error_handler(429, rate_limit_reached)
    main.register_error_handler(404, handle_not_found)
    main.run(debug=True, host='0.0.0.0')
