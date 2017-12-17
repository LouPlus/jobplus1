from flask import Flask,render_template
from flask_migrate import Migrate
from flask_login import LoginManager

from jobplus.models import db
from jobplus.config import configs

#注册蓝图的函数
def register_blueprints(app):
    pass


#用于将flask拓展注册到app
def register_extensions(app):
    db.init_app(app)
    Migrate(app,db)

def create_app(config):
    """可以根据传入的config名称,加载不同的配置
    　　App工厂
    """
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    #SQLAlchemy的初始化方式改为使用init_app
    register_extensions(app)
    #注册蓝图
    register_blueprints(app)

    return app
