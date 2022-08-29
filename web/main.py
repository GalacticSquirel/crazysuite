from flask import Flask , request, jsonify
import os
from git.cmd import Git
from git.repo import Repo

app = Flask(__name__)

# SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
#     username="csuite",
#     password="ez37nWS6Z6DfsrA",
#     hostname="csuite.mysql.eu.pythonanywhere-services.com",
#     databasename="the database name you chose, probably csuite$default",
# )
# app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
# app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

@app.route('/')
def hello_world():
    return jsonify({"message" : "This website does not have a homepage"})

@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        os.system("git reset --hard HEAD")
        repopull = Git().pull('https://github.com/GalacticSquirel/crazysuite.git')

        return jsonify({"message" : str(repopull)})
    else:
        return jsonify({"error" : "Failed"})


app.run()