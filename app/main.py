from flask import Flask, redirect, url_for, request, jsonify, render_template, g
from VersionScraper import get_versions
from AlternateScraper import get_alternatives
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_cors import CORS
import json
import re
import os

app = Flask(__name__)
CORS(app)
if os.environ.get('DATABASE_URL') is None:
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///versions.sqlite3'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/deep'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = "THIS IS SECRET"

db = SQLAlchemy(app)

class Prebirth(db.Model):
	__tablename__ = 'Prebirth'

	id = db.Column('artcile_id', db.Integer, primary_key=True)
	month_no = db.Column(db.Integer)
	article = db.Column(db.String)
	dos = db.Column(db.String)
	donts = db.Column(db.String)
	diet = db.Column(db.String)


class Postbirth(db.Model):
	__tablename__ = 'Postbirth'

	id = db.Column('article_id', db.Integer, primary_key=True)
	month_no = db.Column(db.Integer)
	article = db.Column(db.String)
	dos = db.Column(db.String)
	donts = db.Column(db.String)
	diet = db.Column(db.String)

class Blog(db.Model):
	__tablename__ = 'Blogs'

	id = db.Column('blog_id', db.Integer, primary_key=True)
	author_name = db.Column(db.String)
	article = db.Column(db.String)
	timestamp = db.Column(db.DateTime)
	keywords = db.String(db.String)


