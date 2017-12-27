from flask import Blueprint,render_template,flash,redirect,url_for
from flask import current_app,request
from flask_login import login_user,logout_user,login_required
from jobplus.models import Job

job = Blueprint('job',__name__, url_prefix='/jobs')

@job.route('/')
def job_index():
    page = request.args.get('page', default=1, type=int)
    jobs = Job.query.paginate(page=page, per_page=current_app.config['INDEX_PER_PAGE'],
                              error_out=False)
    return render_template('job/job.html', pagination=jobs)

@job.route('/<int:job_id>')
def detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job/detail.html', job=job)