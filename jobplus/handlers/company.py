from flask import Blueprint,render_template,flash,redirect,url_for
from flask import current_app,request, abort
from flask_login import login_user,logout_user,login_required, current_user
from jobplus.models import Company,Job,db, Send
from jobplus.decorators import company_required
from jobplus.forms import JobForm


company = Blueprint('company', __name__, url_prefix='/companies')

#显示企业列表
@company.route('/')
def company_index():
    page = request.args.get('page', default=1, type=int)
    company = Company.query.paginate(page=page, per_page=current_app.config['INDEX_PER_PAGE'],
                              error_out=False)
    return render_template('company/company.html', pagination=company, active='company')

#显示企业详情
@company.route('/<int:company_id>')
def detail(company_id):
    company = Company.query.get_or_404(company_id)
    jobs = Job.query.filter_by(company_id=company_id)
    return render_template('company/detail.html', company=company,jobs=jobs)

#进去企业管理界面
@company.route('/admin')
@company_required
def admin_base():
    return render_template('company/admin_base.html')

# 显示所有职位(职位管理页面)
@company.route('/admin/<int:company_id>')
@company_required
def admin_index(company_id):
    if not current_user.company.id == company_id:
        abort(404)
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.filter_by(company_id=company_id).paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
        )
    return render_template('company/admin_index.html', company_id=company_id, pagination=pagination)

# 添加职位
@company.route('/job/new', methods=['GET', 'POST'])
@company_required
def create_job():
    form = JobForm()
    if form.validate_on_submit():
        form.create_job(current_user)
        flash('工作创建成功','success')
        return redirect(url_for('company.create_job'))
    return render_template('company/create_job.html',form=form)

# 修改工作要求
@company.route('/job/edit/<int:job_id>', methods=['GET', 'POST'])
@company_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id) #首先找到当前要修改的job
    if not current_user.company.id == job.company_id:
        abort(404)
    form = JobForm(obj=job)
    if form.validate_on_submit():
        form.edit_job(job_id) #传入要修改的job_id
        flash('工作更新成功','success')
        return redirect(url_for('company.edit_job',job_id=job_id))
    return render_template('company/edit_job.html', form=form, job=job)

#删除职位
@company.route('/job/delete/<int:job_id>')
@company_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash('工作删除成功', 'success')
    return redirect(url_for('company.admin_index',company_id=current_user.company.id))

# 面试管理页面
@company.route('/job/<int:company_id>/apply/todolist')
@company_required
def send_index(company_id):
    if not current_user.company.id == company_id:
        abort(404)
    page = request.args.get('page', default=1, type=int)
    pagination = Send.query.filter_by(company_id=current_user.company.id).paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
        )
    return render_template('company/resume_index.html', company_id=current_user.company.id, pagination=pagination)

# 拒绝页面，拒绝申请的面试请求
@company.route('/job/<int:send_id>/reject')
@company_required
def send_reject(send_id):
    send = Send.query.filter_by(id=send_id).first()
    send.qualify = 'REFUSE' #拒绝
    db.session.add(send)
    db.session.commit()
    page = request.args.get('page', default=1, type=int)
    pagination = Send.query.filter_by(company_id=current_user.company.id).paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
        )
    return render_template('company/resume_index.html', company_id=current_user.company.id, pagination=pagination)

# 接受面试的请求
@company.route('/job/<int:send_id>/interview')
@company_required
def send_interview(send_id):
    send = Send.query.filter_by(id=send_id).first()
    send.qualify = 'ACCEPT' #接受
    db.session.add(send)
    db.session.commit()
    page = request.args.get('page', default=1, type=int)
    pagination = Send.query.filter_by(company_id=current_user.company.id).paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
        )
    return render_template('company/resume_index.html', company_id=current_user.company.id, pagination=pagination)