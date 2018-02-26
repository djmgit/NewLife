from flask import Flask, redirect, url_for, request, jsonify, render_template, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
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
    author_email = db.Column(db.String)
    author_name = db.Column(db.String)
    title = db.Column(db.String)
    article = db.Column(db.String)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    keywords = db.Column(db.String)

    def __init__(self, author_email='', author_name='', article='', title='', keywords=''):
        self.author_email = author_email
        self.author_name = author_name
        self.article = article
        self.title = title
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

    def __repr__(self):
        return '<User %r>' % self.email
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.email)


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

class UsersView(ModelView):
    can_create = False
    can_view_details = True

# setup admin
admin = Admin(app, name='NewLife', template_mode='bootstrap3')
admin.add_view(PrebirthView(Prebirth, db.session))
admin.add_view(PostbirthView(Postbirth, db.session))
admin.add_view(BlogView(Blog, db.session))
admin.add_view(UsersView(Users, db.session))

# setup authentication
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(email):
    return Users.query.filter_by(email=email).first()

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
def blogs():
    return render_template('blogs.html')

@app.route('/blogs/add', methods=('GET', 'POST'))
@login_required
def add_blog():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        keywords = request.form['keywords']

        blog = Blog(current_user.email, current_user.first_name + ' ' + current_user.last_name, body, title, keywords)
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('blogs'))
    else:
        return render_template("add_blog.html")

@app.route('/blogs/blog_titles')
def blog_titles():
    blogs = Blog.query.all()
    
    response = []
    response = [{'id': blog.id, 'title': blog.title} for blog in blogs]
    return jsonify({'data': response})

@app.route('/blogs/get_blog/<int:blog_id>')
def get_blog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).all()[0]
    response = {}
    response['author_email'] = blog.author_email
    response['author_name'] = blog.author_name
    response['title'] = blog.title
    response['article'] = blog.article
    response['time_created'] = blog.time_created.strftime("%y-%m-%d-%H-%M")
    response['keywords'] = blog.keywords

    print (response)

    return jsonify({'data': response})


@app.route('/')
def index():
    return 'hello world'

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signup_user', methods=('GET', 'POST'))
def signup_user():
    print (request.form)
    email = request.form['email']
    first_name = request.form['firstname']
    last_name = request.form['lastname']
    password = request.form['pass']

    user = Users.query.filter_by(email=email).first()
    if user:
        return redirect(url_for('signup.html'))
    else:
        new_user = Users(email, first_name, last_name, password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        g.user = current_user
        return redirect(url_for('index'))

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        user = Users.query.filter_by(email=email).first()

        if user:
            if user.password == password:
                login_user(user)
                g.user = current_user
                return redirect(url_for('index'))
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    g.user = None
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


