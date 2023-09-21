from flask import Blueprint,render_template
from ..models.models import *

blue = Blueprint("user",__name__)
@blue.route("/",methods=["GET","POST"])
@blue.route("/index/")
def index():
    categorys = Category.query.all()
    articles = Article.query.all()
    photos = Photo.query.all()
    return render_template("home/index.html",categorys=categorys,articles=articles,photos=photos)

@blue.route("/photos/")
def photos():
    photos = Photo.query.all()
    return render_template("home/photos.html",photos=photos)

@blue.route("/article/")
def articles():
    articles = Article.query.all()
    categorys = Category.query.all()
    return render_template("home/article.html",articles=articles,categorys=categorys)

@blue.route("/about/")
def about():
    photos = Photo.query.all()
    articles = Article.query.all()
    categorys = Category.query.all()
    return render_template("home/about.html",photos=photos,articles=articles,categorys=categorys)
