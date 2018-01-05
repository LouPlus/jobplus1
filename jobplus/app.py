from flask import Flask,render_template
from flask_migrate import Migrate
from flask_login import LoginManager

from jobplus.models import db,User
from jobplus.config import configs
import datetime
#注册蓝图的函数
def register_blueprints(app):
    from .handlers import front,user,job,company,admin
    app.register_blueprint(front)
    app.register_blueprint(user)
    app.register_blueprint(job)
    app.register_blueprint(company)
    app.register_blueprint(admin)

#用于将flask拓展注册到app
def register_extensions(app):
    db.init_app(app)
    Migrate(app,db)

    login_manager = LoginManager()
    login_manager.init_app(app)

    #使用 user_loader 装饰器注册一个函数，用来告诉 flask-login 如何加载用户对象
    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    #用户未登录时,就会被重定向到login_view指定的页面
    login_manager.login_view = 'front.login'

# jinjia里的函数
def register_filters(app):
    @app.template_filter()
    def timesince(value):
        now = datetime.datetime.utcnow()
        delta = now - value
        if delta.days>365:
            return '{}年前'.format(delta.days // 365)
        if delta.days>30:
            return '{}月前'.format(delta.days // 30)
        if delta.days>0:
            return '{}天前'.format(delta.days)
        if delta.seconds>3600:
            return '{}小时前'.format(delta.seconds // 3600)
        if delta.seconds>60:
            return '{}分钟前'.format(delta.seconds // 60)
        return '刚刚'

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
    register_filters(app)

    return app
