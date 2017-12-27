from flask import Blueprint,render_template,flash,redirect,url_for
from flask import current_app,request
from flask_login import login_user,logout_user,login_required

from jobplus.forms import LoginForm, UserRegister,CompanyRegister
from jobplus.models import User,Job,Company

front = Blueprint('front',__name__)

#主页
@front.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    jobs = Job.query.paginate(page=page, per_page=current_app.config['INDEX_PER_PAGE'],
                              error_out=False)
    companies = Company.query.paginate(page=page, per_page=current_app.config['INDEX_PER_PAGE'],
                                       error_out=False)
    return render_template('index.html',pagination=[jobs,companies])


#普通用户注册界面
@front.route('/user_register', methods=['GET','POST'])
def user_register():
    form = UserRegister()
    try:
        form.validate_on_submit()
        form.create_user()
        flash('注册成功,请登录','success')
        return redirect(url_for('front.login')) #注册成功后自动跳转到登录界面
    except:
        flash('注册失败,请重新注册','warning')
    return render_template('register_user.html', form=form)

#企业用户注册界面
@front.route('/company_register', methods=['GET','POST'])
def company_register():
    form = CompanyRegister()
    try:
        form.validate_on_submit()
        form.create_user()
        flash('注册成功,请登录', 'success')
        return redirect(url_for('front.login')) #注册成功后自动跳转到登录界面
    except:
        flash('注册失败,请重新注册','warning')
    return render_template('register_company.html', form=form)

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
