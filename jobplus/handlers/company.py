from flask import Blueprint,render_template,flash,redirect,url_for
from flask import current_app,request
from flask_login import login_user,logout_user,login_required
from jobplus.models import Company,Job

company = Blueprint('company',__name__, url_prefix='/companies')


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