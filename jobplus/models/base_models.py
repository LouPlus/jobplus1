from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import url_for

#这里不要传入app
db = SQLAlchemy()

class Base(db.Model):
    """所有model的一个基类,默认添加时间戳
    """
    # 表示不要把这个类当作 Model 类
    __abstract__ = True
    # 设置了 default 和 onupdate 这俩个时间戳都不需要自己去维护
    created_at = db.Column(db.DateTime,default = datetime.utcnow)
    updated_at = db.Column(db.DateTime,default = datetime.utcnow,onupdate = datetime.utcnow)
