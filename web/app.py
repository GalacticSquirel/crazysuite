
from flask import Blueprint, render_template, flash, send_file, url_for,request,jsonify,redirect
from flask_login import login_required, current_user
from __init__ import create_app, db
import json
from git.cmd import Git
from git.repo import Repo
# import win32gui
# import win32con
import threading
import os
main = Blueprint('main', __name__)

@main.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        os.system("git reset --hard HEAD")
        repopull = Git().pull('https://github.com/GalacticSquirel/crazysuite.git')

        return jsonify({"message" : str(repopull)})
    else:
        return jsonify({"error" : "Failed"})
    
@main.route('/') 
def index():
    return render_template('index.html')

@main.route("/favicon.ico")
def favicon():
    return send_file("templates//favicon.ico", mimetype='image/gif')

@main.route('/account') 
def account():
    return render_template('account.html')

@main.route('/shop')
def shop():
    return render_template("shop.html")

@main.route("/products")
@login_required  
def products():
    return render_template('products.html', name=current_user.name)

@main.route('/login.css')
def logincss():
    return send_file('templates//login.css')

@main.route('/style.css')
def stylecss():
    return send_file('templates//style.css')

@main.route('/account.css')
def accountcss():
    return send_file('templates//account.css')

@main.route("/products.css")
def productscss():
    return send_file("templates//products.css")

app = create_app()


if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(debug=True,host='0.0.0.0') 
    
    
#profile page is controls