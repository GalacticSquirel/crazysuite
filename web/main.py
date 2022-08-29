from flask import Flask , request, jsonify
import os
from git.cmd import Git
from git.repo import Repo
from flask_mysqldb import MySQL
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
app.config['MYSQL_HOST'] = 'csuite.mysql.eu.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'csuite'
app.config['MYSQL_PASSWORD'] = 'ez37nWS6Z6DfsrA'
app.config['MYSQL_DB'] = 'default'

mysql = MySQL(app)

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

@app.route("/login", methods = ['GET', 'POST'])
def login():
    name = request.headers['name']
    age = request.headers['age']
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO info_table VALUES(%s,%s)''',(name,age))
    mysql.connection.commit()
    cursor.close()
    return f"{name,age} inserted"

