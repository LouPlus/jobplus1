from flask import Blueprint,render_template,flash,redirect,url_for
from flask import current_app,request
from flask_login import login_user,logout_user,login_required
from jobplus.decorators import admin_required
from jobplus.models.models import User
from jobplus.forms import UserRegister,CompanyRegister


admin = Blueprint('admin',__name__,url_prefix='/admin')


@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')


@admin.route('/users')
@admin_required
def users():
    page = request.args.get('page',default=1,type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/users.html',pagination=pagination)


@admin.route('/users/adduser',methods=['GET','POST'])
@admin_required
def create_user():
    form = UserRegister()
    if form.validate_on_submit():
        form.create_user()
        flash('用户创建成功','success')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_user.html', form=form)



@admin.route('/users/addcompany',methods=['GET','POST'])
@admin_required
def create_company():
    form = CompanyRegister()
    if form.validate_on_submit():
        form.create_user()
        flash('用户创建成功','success')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_company.html', form=form)