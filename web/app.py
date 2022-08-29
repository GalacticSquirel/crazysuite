
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
    return render_template('home.html')

@main.route("/jquery.js")
def jquery():
    return send_file('templates//jquery.js')

@main.route("/nicepage.js")
def nicepagejs():
    return send_file('templates//nicepage.js')

@main.route('/home')
def homehtml():
    return send_file('templates//home.html')

@main.route("/favicon.ico")
def favicon():
    return send_file("templates//favicon.ico", mimetype='image/gif')

@main.route('/profile') 
def profile():
    return render_template('profile.html')

@main.route('/random')
def random():
    return render_template("random.html")

@main.route('/contact')
def contact():
    return render_template("contact.html")

@main.route('/main.css')
def maincss():
    return send_file('templates//main.css')
@main.route('/login.css')
def logincss():
    return send_file('templates//login.css')

@main.route('/style.css')
def stylecss():
    return send_file('templates//style.css')

@main.route('/profile.css')
def profilecss():
    return send_file('templates//profile.css')

@main.route('/nicepage.css')
def nicepagecss():
    return send_file('templates//nicepage.css')

@main.route("/controls.css")
def controlscss():
    return send_file("templates//controls.css")

@main.route("/monitor-on")
@login_required
def monitoron():
    with open("states.json","r") as f:
        states = json.loads(f.read())
    states["screens"] = "On"
    
    # def send():
    #     win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, 2)
    # t = threading.Thread(target=send)
    # t.start()
    return redirect(url_for("main.controls"))
@main.route("/monitor-off")
@login_required
def monitoroff():
    with open("states.json","r") as f:
        states = json.loads(f.read())
    states["screens"] = "Off"
    
    # def send():
    #     win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, 1)
    # t = threading.Thread(target=send)
    # t.start()
    return redirect(url_for("main.controls"))
    
app = create_app()
@main.route("/controls")
@login_required  
def controls():
    with open("states.json","r") as f:
        states = json.loads(f.read())
    print(states)
    return render_template('controls.html', name=current_user.name, comp_state=states["computer"], screen_state=states["screens"],on_url=url_for("main.monitoron"))

if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(debug=True,host='0.0.0.0') 
    
    
#profile page is controls