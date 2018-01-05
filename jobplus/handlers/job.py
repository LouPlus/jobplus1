from flask import Blueprint,render_template,flash,redirect,url_for
from flask import current_app,request, abort
from flask_login import login_user,logout_user,login_required,current_user
from jobplus.models import Job,Send,db


job = Blueprint('job',__name__, url_prefix='/jobs')

#职位列表
@job.route('/')
def job_index():
    page = request.args.get('page', default=1, type=int)
    jobs = Job.query.paginate(page=page, per_page=current_app.config['INDEX_PER_PAGE'],
                              error_out=False)
    return render_template('job/job.html', pagination=jobs,active='job')

#职位详情
@job.route('/<int:job_id>')
def detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job/detail.html', job=job)

#投递简历页面
@job.route('/<int:job_id>/apply')
def apply(job_id):
    job = Job.query.get_or_404(job_id)
    if current_user.employee.resume is None:
        flash('请上传简历','warnning')
    elif job.current_user_is_send:
        flash('已投递过简历','warning')
    else:
        send = Send(
            job_id=job.id,
            company_id = job.company.id,
            user_id = current_user.id
        )
        db.session.add(send)
        db.session.commit()
        flash('投递成功','success')
    return redirect(url_for('job.detail',job_id=job.id))

#职位下线
@job.route('/<int:job_id>/disable')
def disable(job_id):
    job = Job.query.get_or_404(job_id)
    if not current_user.is_admin and current_user.company.id != job.company_id:
        abort(404)
    if job.is_disable:
        flash('已下线', 'warning')
    else:
        job.is_disable=True
        db.session.add(job)
        db.session.commit()
        flash('下线成功', 'success')
    if current_user.is_admin:
        return redirect(url_for('admin.jobs'))
    else:
        return redirect(url_for('company.admin_index', company_id=job.company.id))
    

#职位上线
@job.route('/<int:job_id>/enable')
def enable(job_id):
    job = Job.query.get_or_404(job_id)
    if not current_user.is_admin and current_user.company.id != job.company_id:
        abort(404)
    if job.is_disable:
        job.is_disable=False
        db.session.add(job)
        db.session.commit()
        flash('上线成功', 'success')
    else:
        flash('已上线', 'warning')
    if current_user.is_admin:
        return redirect(url_for('admin.jobs'))
    else:
        return redirect(url_for('company.admin_index', company_id=job.company.id))

