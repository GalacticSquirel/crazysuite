
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
@login_required
def account():
    return render_template('account.html', name=current_user.name)



@main.route('/shop')
def shop():
    def add_url(x):
        x["url"] = url_for("main.productdetails", **x)
        return x
    shop_items = [{"name": "Product 1", "description": "description of product 1 be like","price": "£9.99","genre": "Software",
                   "image_url": url_for('main.images', image_name='product1'), "big_image_url": url_for('main.images', image_name='product1')},
                  {"name": "Product 2", "description": "description of product 2 be like something else","price": "£9.90","genre": "Software",
                   "image_url": url_for('main.images', image_name='product1'), "big_image_url": url_for('main.images', image_name='product1')}, 
                  {"name": "Product 3", "description": "description of product 3 be like something that isnt product 7","price": "£5.99","genre": "Software",
                   "image_url": url_for('main.images', image_name='product1'), "big_image_url": url_for('main.images', image_name='product1')},
                  {"name": "Product 4", "description": "description of product 4 be like something that isnt product 6","price": "£3.99","genre": "Software",
                   "image_url": url_for('main.images', image_name='product1'), "big_image_url": url_for('main.images', image_name='product1')},
                  {"name": "Product 5", "description": "description of product 5 be like something that isnt product 5","price": "£6.99","genre": "Software",
                   "image_url": url_for('main.images', image_name='product1'), "big_image_url": url_for('main.images', image_name='product1')},
                  {"name": "Product 6", "description": "description of product 6 be like something that isnt product 4","price": "£7.99","genre": "Software",
                   "image_url": url_for('main.images', image_name='product1'), "big_image_url": url_for('main.images', image_name='product1')},
                  {"name": "Product 7", "description": "description of product 7 be like something that isnt product 3","price": "£2.99","genre": "Software",
                   "image_url": url_for('main.images', image_name='product1'), "big_image_url": url_for('main.images', image_name='product1')}]
    with_urls = list(map(lambda x: add_url(x), shop_items))
    return render_template("shop.html", shop_items=with_urls)

@main.route("/productdetails/")
def productdetails():

    item_details = {"name": request.args.get('name', default = 1, type = str),
                    "description": request.args.get('description', default = 1, type = str),
                    "genre": request.args.get('genre', default = 1, type = str),
                    "image_url": request.args.get('image_url', default = 1, type = str),
                    "price": request.args.get('price', default = 1, type = str),
                    "big_image_url": request.args.get('big_image_url', default = 1, type = str)}

    return render_template("productdetails.html", item_details=item_details)

@main.route("/productdetails/productdetails.css")
def product_detailscss():
    return send_file("templates//productdetails.css")

@main.route("/signup.css")
def signupcss():
    return send_file("templates//signup.css")

@main.route("/productdetails/style.css")
def product_detailsstylecss():
    return send_file("templates//style.css")

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

@main.route('/home.css')
def homecss():
    return send_file('templates//index.css')

@main.route("/products.css")
def productscss():
    return send_file("templates//products.css")

@main.route("/shop.css")
def shopcss():
    return send_file("templates//shop.css")

@main.route("/images/<image_name>")
def images(image_name):
    if str(image_name) +".png" in os.listdir("templates//images"):
        return send_file(f"templates//images//{image_name}.png")
    else:
        return send_file(f"templates//images//place_hold.png")

app = create_app()

if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(debug=True,host='0.0.0.0') 
    
    
#profile page is controls