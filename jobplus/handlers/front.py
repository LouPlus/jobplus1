from flask import Blueprint,render_template,flash,redirect,url_for
from flask import current_app,request
from flask_login import login_user,logout_user,login_required

from jobplus.forms import LoginForm, UserRegister
from jobplus.models import User

front = Blueprint('front',__name__)

#主页
@front.route('/')
def index():
    return render_template('index.html')

#注册界面
@front.route('/register', methods=['GET','POST'])
def register():
    form = UserRegister()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功,请登录','success')
        return redirect(url_for('front.login')) #注册成功后自动跳转到登录界面
    return render_template('register_user.html', form=form)

#登录界面
@front.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        
        login_user(user,form.remember_me.data)
        flash("欢迎用户"+form.name.data+"登录~~~","success")
        return redirect(url_for('front.index'))#若登录成功则返回主页

    return render_template('login.html',form=form)

# 退出页面注册
@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经退出登录','success')
    return redirect(url_for('front.index'))
