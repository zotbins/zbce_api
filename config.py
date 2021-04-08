import os
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# load environment variables
dotenv_path = Path("/var/www/app/app/.env") # use absolute path with LAMP server implementation, change to relative path when testing w/ a Flask development server
load_dotenv(dotenv_path=dotenv_path)

SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

# for your upload folder make sure you change the permissions so anyone can modify it using `chmod 777`
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True # turn this off when not debugging.

db = SQLAlchemy(app)
