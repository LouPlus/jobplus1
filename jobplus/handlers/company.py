from flask import Blueprint,render_template,flash,redirect,url_for
from flask import current_app,request
from flask_login import login_user,logout_user,login_required


company = Blueprint('company',__name__)


@company.route('/')
def index():
    return render_template('company/index.html')
