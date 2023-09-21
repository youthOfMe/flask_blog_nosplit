from flask import Flask
from .views.views import blue
from .exts import  init_exts
from .views.views_admin import admin

def create_app():
    print(type(admin))
    app = Flask(__name__)
    app.register_blueprint(blueprint=blue)
    app.register_blueprint(blueprint=admin)

    #配置数据库
    # 采用MySQL关系型数据库
    db_uri = "mysql+pymysql://root:123456@127.0.0.1:3306/new_blog"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    #初始化插件
    init_exts(app=app)

    return app