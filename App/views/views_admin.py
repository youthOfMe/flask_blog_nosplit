from ..models.models_admin import *
from ..models.models import *
import requests
from ..exts import db
from flask import Blueprint,render_template,request,redirect,jsonify
from functools import wraps
import time


admin = Blueprint("admin",__name__)

def login_requried(fn):
    def inner(*args,**kwargs):
        username = request.cookies.get("username")
        for admin_info in AdminUser.query.all() :
            if username == admin_info.name :
                request.username = username
                return fn(*args,**kwargs)
        return redirect("/admin/login/")
    return inner

@admin.route("/admin/login/",methods=["POST","GET"],endpoint="login")
def login() :
    username = request.form.get("username")
    userpwd = request.form.get("userpwd")
    admin_info_list = AdminUser.query.all()
    for admin_info in admin_info_list :
        if admin_info.name == username and admin_info.passwd == userpwd :
            response = redirect("/admin/index/")
            response.set_cookie("username",username)
            return response
        else :
            return render_template("admin/login.html")

@admin.route("/admin/")
@admin.route("/admin/index/",endpoint="admin_index")
@login_requried
def admin_index() :
    username = request.username
    categorys = Category.query.filter()
    categorys_count = categorys.count()
    articles = Article.query.filter()
    articles_count = articles.count()
    photos = Photo.query.filter()
    photos_count = photos.count()
    return render_template("admin/index.html",username=username,categorys_count=categorys_count
                           ,articles_count=articles_count,photos_count=photos_count)

@admin.route("/admin/logout/",endpoint="logout")
@login_requried
def logout():
    request.username = None
    response = redirect("/admin/login/")
    response.delete_cookie("username")
    return response

# 分类管理
@admin.route("/admin/category/",endpoint="admin_category",methods=["GET","POST"])
@login_requried
def admin_category():
    categorys = Category.query.all()
    if request.method == "GET":
        return render_template("admin/category.html",categorys=categorys)
    elif request.method == "POST":
        category_name = request.form.get("name")
        category_describe = request.form.get("describe")
        if category_name and category_describe :
            category = Category()
            category.name = category_name
            category.describe = category_describe
            try :
                db.session.add(category)
                db.session.commit()
                db.session.flush()
                print("牛马你成功啦")
                return redirect("/admin/category/")
            except Exception as e:
                print(e,"数据库提交错误")
                db.session.rollback()
                db.session.flush()
                return "添加数据失败"

# 删除分类功能
@admin.route("/admin/delete_category/",endpoint="admin_category_delete",methods=["GET","POST"])
@login_requried
def admin_category_delete():
    id = request.form.get("id")
    category_item = Category.query.get(id)
    try :
        db.session.delete(category_item)
        db.session.commit()
    except Exception as e:
        print(e,"删除数据库失败")
        db.session.rollback()
        db.session.flush()
    return jsonify({"code":200,"msg":"删除成功"})

@admin.route("/admin/category_update/<id>/",endpoint="admin_category_update",methods=["GET","POST"])
@login_requried
def admin_category_update(id):
    category_item = Category.query.get(id)
    if request.method == "GET":
        return render_template("admin/category_update.html",category_item=category_item)
    elif request.method == "POST":
        try :
            category_item_name = request.form.get("name")
            category_item_decribe = request.form.get("describe")
            category_item.name = category_item_name
            category_item.describe = category_item_decribe
            db.session.commit()
            return redirect("/admin/category/")
        except Exception as e:
            print(e,"s")
            db.session.rollback()
            db.session.flush()

# -------------------------文章管理--------------
@admin.route("/admin/article/",endpoint="admin_article")
@login_requried
def admin_article():
    articles = Article.query.all()
    return render_template("admin/article.html",articles=articles)

@admin.route("/admin/add_article/",endpoint="admin_article_add",methods=["GET","POST"])
@login_requried
def admin_article_add():
    if request.method == "GET":
        categorys = Category.query.all()
        return render_template("admin/article_add.html",categorys=categorys)
    elif request.method == "POST":
        args = request.form
        title = args.get("title")
        keyword = args.get("keywords")
        content = args.get("content")
        category = args.get("category")
        # 获取上传的图片
        img = request.files.get("img")
        # 图片存储路径 存储图片
        img_name = f"{time.time()} - {img.filename}"
        img_url = f"/static/home/uploads/{img_name}"
        try :
            article = Article()
            article.title = title
            article.keyword = keyword
            article.content = content
            article.category_id = category
            article.img = img_url
            db.session.add(article)
            db.session.commit()
            print("提交成功")
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            print(e,"提交失败请检查")
        else :
            img_data = img.read() # 读取图片对象里面的数据
            with open(f"App{img_url}","wb") as fp:
                fp.write(img_data)
                fp.flush()

        return redirect("/admin/article/")

# 删除文章
@admin.route("/admin/delete_article/<id>/",endpoint="admin_article_delete")
@login_requried
def admin_article_delete(id):
    article_item = Article.query.get(id)
    try :
        db.session.delete(article_item)
        db.session.commit()
        print("提交成功")
    except Exception as e:
        print(e,'数据删除失败')
        db.session.rollback()
        db.session.flush()
    return redirect("/admin/article/")

# 修改文章
@admin.route("/admin/update_article/<id>/",endpoint="admin_article_update",methods=["GET","POST"])
@login_requried
def admin_article_update(id):
    article_item = Article.query.get(id)
    if request.method == "GET":
        categorys = Category.query.all()
        return render_template("admin/article_update.html",article_item=article_item,
                               categorys=categorys)
    elif request.method == "POST":
        args = request.form
        print(args)
        title = args.get("title")
        keyword = args.get("keywords")
        content = args.get("content")
        category_id = args.get("category")
        img = request.files.get("img")
        img_name = img.filename
        img_url = f"/static/home/uploads/{time.time()} - {img_name}"

        try :
            article_item.title = title
            article_item.keyword = keyword
            article_item.content = content
            article_item.category_id = category_id
            article_item.img = img_url
            db.session.commit()
            print("提交成功")
        except Exception as e:
            print(e,"提交失败")
            db.session.rollback()
            db.session.flush()
        else :
            img_data = img.read()  # 读取图片对象里面的数据
            with open(f"App{img_url}", "wb") as fp:
                fp.write(img_data)
                fp.flush()
        return redirect("/admin/article/")





