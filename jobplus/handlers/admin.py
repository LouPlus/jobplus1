from flask import Blueprint,render_template,flash,redirect,url_for
from flask import current_app,request
from flask_login import login_user,logout_user,login_required
from jobplus.decorators import admin_required
from jobplus.models.models import User
from jobplus.forms import UserRegister,CompanyRegister,AdminRegister,UserProfile,AdminProfile,CompanyProfile


admin = Blueprint('admin',__name__,url_prefix='/admin')

#用户管理界面
@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

#管理用户
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

#增加用户
@admin.route('/users/adduser',methods=['GET','POST'])
@admin_required
def create_user():
    form = UserRegister()
    if form.validate_on_submit():
        form.create_user()
        flash('用户创建成功','success')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_user.html', form=form)


#增加企业
@admin.route('/users/addcompany',methods=['GET','POST'])
@admin_required
def create_company():
    form = CompanyRegister()
    if form.validate_on_submit():
        form.create_user()
        flash('用户创建成功','success')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_company.html', form=form)

#修改求职者用户的信息
@admin.route('/user_profile/<int:user_id>', methods=['GET','POST'])
@login_required
def user_profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    form = UserProfile()
    form.name.data = user.name
    form.email.data = user.email
    form.image.data = user.logo_img
    form.sex.data = user.employee.sex.name
    form.location.data = user.employee.location
    form.description.data = user.employee.description
    form.resume.data = user.employee.resume
    if form.validate_on_submit():
        form.updated_profile(user)
        flash('简历已更新成功','success')
        return redirect(url_for('admin.user_profile',user_id=user.id))
    return render_template('admin/profile.html',form=form,user=user)

#修改管理员信息
@admin.route('/admin_profile/<int:user_id>', methods=['GET','POST'])
@login_required
def admin_profile(user_id):#修改求职者用户的信息
    user = User.query.filter_by(id=user_id).first()
    form = AdminProfile()
    form.name.data = user.name
    form.email.data = user.email
    form.image.data = user.logo_img
    if form.validate_on_submit():
        form.updated_profile(user)
        flash('简历已更新成功','success')
        return redirect(url_for('user.admin_profile',user_id=user.id))
    return render_template('admin/profile.html',form=form,user=user)

#修改企业用户的信息
@admin.route('/company_profile/<int:user_id>', methods=['GET','POST'])
@login_required
def company_profile(user_id):#修改求职者用户的信息
    user = User.query.filter_by(id=user_id).first()
    form = CompanyProfile()
    form.name.data = user.name
    form.email.data = user.email
    form.image.data = user.logo_img
    form.web.data = user.company.website
    form.oneword.data = user.company.oneword
    form.description.data = user.company.description
    if form.validate_on_submit():
        form.updated_profile(user)
        flash('简历已更新成功','success')
        return redirect(url_for('user.company_profile',user_id=user.id))
    return render_template('admin/profile.html',form=form,user=user)