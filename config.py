import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# for your upload folder make sure you change the permissions so anyone can modify it using `chmod 777`
UPLOAD_FOLDER = '.' #change this to your specified upload folder
ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'YOUR_HARD_TO_GUESSS_STRING'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://YOUR_MYSQL_USERNAME_HERE:YOUR_MYSQL_PASSWORD_HERE@localhost/zotbinsCE'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True # turn this off when not debugging.

db = SQLAlchemy(app)
