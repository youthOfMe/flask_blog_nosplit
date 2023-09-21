# 构建数据表结构
from ..exts import db

class Category(db.Model):
    __tablename__ = "tb_category"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(60),unique=True)
    describe = db.Column(db.Text())
    # 使用类目和文章进行建立联系
    articles = db.relationship("Article",backref="category",lazy="dynamic")

class Article(db.Model):
    __tablename__ = "tb_article"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(90))
    keyword = db.Column(db.String(255))
    content = db.Column(db.Text())
    img = db.Column(db.Text())
    # 使用外键连接分类中的类目id
    category_id = db.Column(db.Integer,db.ForeignKey(Category.id))

class Photo(db.Model):
    __tablename__ = "tb_photo"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    url = db.Column(db.Text())
    name = db.Column(db.String(60))
    describe = db.Column(db.Text())

