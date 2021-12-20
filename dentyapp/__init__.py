
#This file will import all the things we need in this package so that it #will be assessible to any module in the package, any module can import as #from thispackage import xx '''

from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mysql_connector import MySQL

#from flask_wtf.csrf import CSRFProtect
UPLOAD_FOLDER = 'static/dentyimages/'

app = Flask(__name__,instance_relative_config=True)
# app.config['DEBUG'] = True

#csrf = CSRFProtect()  #or use this method csrf.init_app(app)

#load the package's config here after the app has been created

from dentyapp import config #config within package folder
app.config.from_object(config.LiveConfig)
app.config.from_pyfile('config.py') #loads config from instance folder
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']
app.config['UPLOAD_PATH'] = 'dentyapp/static/recipients_images'
app.config['MYSQL_USER'] = 'debbie2'
app.config['MYSQL_DATABASE'] = 'denty'
db = SQLAlchemy(app)
mysql = MySQL(app)

#Routes are now separated, load routes each from the respective folder
from myroutes import admin,user

from dentyapp import forms
from dentyapp import mymodel

