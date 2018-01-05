from flask import Blueprint,render_template,flash,redirect,url_for
from flask import current_app,request, abort
from flask_login import login_user,logout_user,login_required, current_user
from jobplus.models import Company,Job,db, Send
from jobplus.decorators import company_required
from jobplus.forms import JobForm


company = Blueprint('company', __name__, url_prefix='/companies')


@company.route('/')
def company_index():
    page = request.args.get('page', default=1, type=int)
    company = Company.query.paginate(page=page, per_page=current_app.config['INDEX_PER_PAGE'],
                              error_out=False)
    return render_template('company/company.html', pagination=company, active='company')

@company.route('/<int:company_id>')
def detail(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template('company/detail.html', company=company)


@company.route('/admin')
@company_required
def admin_base():
    return render_template('company/admin_base.html')


@company.route('/<int:company_id>/admin')
@company_required
def admin_index(company_id):
    if not current_user.id == company_id:
        abort(404)
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.filter_by(company_id=company_id).paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
        )
    return render_template('company/admin_index.html', company_id=company_id, pagination=pagination)


@company.route('/job/new', methods=['GET', 'POST'])
@company_required
def create_job():
    form = JobForm()
    if form.validate_on_submit():
        form.create_job(current_user)
        flash('工作创建成功','success')
        return redirect(url_for('company.admin_index',company_id=current_user.id))
    return render_template('company/create_job.html',form=form)

@company.route('/job/<int:job_id>/edit', methods=['GET', 'POST'])
@company_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    if not current_user.id == job.company_id:
        abort(404)
    form = JobForm(obj=job)
    if form.validate_on_submit():
        form.edit_job(job)
        flash('工作更新成功','success')
        return redirect(url_for('company.admin_index',company_id=current_user.id))
    return render_template('company/edit_job.html', form=form, job=job)


@company.route('/job/<int:job_id>/delete')
@company_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash('工作删除成功', 'success')
    return redirect(url_for('company.admin_index',company_id=current_user.id))


@company.route('/job/<int:company_id>/apply/todolist')
@company_required
def send_index(company_id):
    if not current_user.id == company_id:
        abort(404)
    page = request.args.get('page', default=1, type=int)
    pagination = Send.query.filter_by(company_id=current_user.company.id).paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
        )
    return render_template('company/resume_index.html', company_id=current_user.company.id, pagination=pagination)


@company.route('/job/<int:send_id>/reject')
@company_required
def send_reject(send_id):
    send = Send.query.filter_by(id=send_id).first()
    send.qualify = 'REFUSE'
    db.session.add(send)
    db.session.commit()
    page = request.args.get('page', default=1, type=int)
    pagination = Send.query.filter_by(company_id=current_user.company.id).paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
        )
    return render_template('company/resume_index.html', company_id=current_user.company.id, pagination=pagination)


@company.route('/job/<int:send_id>/interview')
@company_required
def send_interview(send_id):
    send = Send.query.filter_by(id=send_id).first()
    send.qualify = 'ACCEPT'
    db.session.add(send)
    db.session.commit()
    page = request.args.get('page', default=1, type=int)
    pagination = Send.query.filter_by(company_id=current_user.company.id).paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
        )
    return render_template('company/resume_index.html', company_id=current_user.company.id, pagination=pagination)