from flask import Flask, redirect, url_for, request, jsonify, render_template, g
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_cors import CORS
from Serialiser import *
from marshmallow import pprint
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
    title = db.Column(db.String)
    article = db.Column(db.String)
    dos = db.Column(db.String)
    donts = db.Column(db.String)
    diet = db.Column(db.String)

    def __init__(self, month_no='', title='', article='', dos='', donts='', diet=''):
        self.month_no = month_no
        self.title = title
        self.article = article
        self.dos = dos
        self.donts = donts
        self.diet = diet


class Postbirth(db.Model):
    __tablename__ = 'Postbirth'

    id = db.Column('article_id', db.Integer, primary_key=True)
    month_no = db.Column(db.Integer)
    title = db.Column(db.String)
    article = db.Column(db.String)
    dos = db.Column(db.String)
    donts = db.Column(db.String)
    diet = db.Column(db.String)

    def __init__(self, month_no='', title='', article='', dos='', donts='', diet=''):
        self.month_no = month_no
        self.title = title
        self.article = article
        self.donts = donts
        self.dos = dos
        self.diet = diet

class Blog(db.Model):
    __tablename__ = 'Blogs'

    id = db.Column('blog_id', db.Integer, primary_key=True)
    author_name = db.Column(db.String)
    title = db.Column(db.String)
    article = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    keywords = db.String(db.String)

    def __init__(self, author_name='', article='', title='', timestamp='', keywords=''):
        self.author_name = author_name
        self.article = article
        self.title = title
        self.timestamp = timestamp
        self.keywords = keywords

class Users(db.Model):
    __tablename__ = 'Users'

    id = db.Column('user_id', db.Integer, primary_key=True)
    email = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, email='', first_name='', last_name='', password=''):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password


db.create_all()

class PrebirthView(ModelView):
    can_create = True
    can_view_details = True    
    edit_modal = True

class PostbirthView(ModelView):
    can_create = True
    can_view_details = True    
    edit_modal = True

class BlogView(ModelView):
    can_create = False
    can_view_details = True

# setup admin
admin = Admin(app, name='NewLife', template_mode='bootstrap3')
admin.add_view(PrebirthView(Prebirth, db.session))
admin.add_view(PostbirthView(Postbirth, db.session))
admin.add_view(BlogView(Blog, db.session))

@app.route('/api/prebirth_articles/<int:month_no>')
def show_prebirth_article(month_no):
    prebirth_article = Prebirth.query.filter_by(month_no=month_no).all()[0]
    response = {}
    prebirth_schema = PrebirthSchema()
    data = prebirth_schema.dumps(prebirth_article)
    data = json.loads(data.data)
    return jsonify({'data':data})

@app.route('/api/postbirth_articles/<int:month_no>')
def show_postbirth_article(month_no):
    postbirth_article = Postbirth.query.filter_by(month_no=month_no).all()[0]
    response = {}
    postbirth_schema = PostbirthSchema()
    data = postbirth_schema.dumps(postbirth_article)
    data = json.loads(data.data)
    return jsonify({'data':data})

@app.route('/prebirth')
def prebirth():
    return render_template("prebirth.html")

@app.route('/postbirth')
def postbirth():
    return render_template("postbirth.html")

@app.route('/blogs')
def show_blogs():
    return "blogs"

@app.route('/blogs/add')
def add_blog():
    return render_template("add_blog.html")


@app.route('/')
def index():
    return 'hello world'

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signup_user')
def signup_user():
    email = request.form['email']
    first_name = request.form['firstname']
    last_name = request.form['lastname']
    password = request.form['pass']

    user = Users.query.filter_by(email=email).first()
    if user:
        return redirect(url_for('signup.html'))
    else:
        new_user = Users(email, firstname, lastname, password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))



@app.route('/login')
def login():
    return 'login'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


