from ..exts import db

class AdminUser(db.Model):
    __tablename__ = "tb_admin_user"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(60))
    passwd = db.Column(db.String(60))
