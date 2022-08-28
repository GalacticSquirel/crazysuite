from flask import Flask , request, jsonify
import os
from git.cmd import Git 
from git.repo import Repo
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        os.system("git reset --hard HEAD")
        repopull = Git().pull('https://github.com/GalacticSquirel/crazysuite.git')

        return jsonify({"message" : str(repopull)})
    else:
        return jsonify({"message" : "Failed"})

app.run()