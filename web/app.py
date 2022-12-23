
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
    return redirect('/home')

@main.route('/home')
def home():
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
    shop_items = json.load(open("static/items.json", "r"))
    with_urls = list(shop_items)
    return render_template("shop.html", shop_items=with_urls)

@main.route('/shop/<string:item_name>')
def productdetails(item_name):
    addresses = []
    shop_items = json.load(open("static/items.json", "r"))
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
    return render_template("productdetails.html", item_details=item_details)

@main.route("/shop/productdetails.css")
def product_detailscss():
    return send_file("templates//productdetails.css")

@main.route('/shop/style.css')
def product_detailsstylecss():
    return send_file('templates//style.css')

@main.route("/signup.css")
def signupcss():
    if not current_user.is_authenticated:
        return send_file("templates//signup.css")
    else:
        return redirect('/')

@main.route('/login.css')
def logincss():
    if not current_user.is_authenticated:
        return send_file('templates//login.css')
    else:
        return redirect('/')

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

@main.route('/404.css')
def error404css():
    return send_file('templates//404.css')

@main.route("/shop.css")
def shopcss():
    return send_file("templates//shop.css")

@main.route("/images/<image_name>")
def images(image_name):
    if str(image_name) +".png" in os.listdir("templates//images"):
        return send_file(f"templates//images//{image_name}.png")
    else:
        return send_file(f"templates//images//place_holder.png")

from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    print(f"dd {filename}")
    return True if filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS else False

@main.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.id in [1,2]:
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if allowed_file(file.filename):
                print(file)
                file.save(f"templates/images/{file.filename}")
            return redirect(url_for('main.admin'))
        return render_template("console.html")
    else:
        return redirect("/")
    
    
@main.route("/admin/add", methods=['GET', 'POST'])
@login_required
def add():
    if current_user.id in [1,2]:
        form = request.form
        info ={"name": form.get("name"), "page_name": form.get("page_name"), "description": form.get("description"), "full_description": form.get("full_description"), "price": form.get("price"), "genre": form.get("genre")}
        # info = list(map(lambda x: form.get(x), info_names))
        info["image_url"] = (url_for('main.images', image_name=form.get("image_name")))
        info["big_image_url"] = (url_for('main.images', image_name=form.get("big_image_name")))
        
        with open("static/items.json", "r") as f:
            curr_items = json.load(f)

        curr_items.append(info)
        with open("static/items.json", "w") as f:
            json.dump(curr_items, f)
        print(info)
        return redirect(url_for('main.admin'))
    else:
        return redirect("/")

@main.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

app = create_app()

if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(debug=True,host='0.0.0.0') 
    
    
#profile page is controls