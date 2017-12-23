from flask import Blueprint,render_template,flash,redirect,url_for
from flask import current_app,request
from flask_login import login_user,logout_user,login_required, current_user
from jobplus.models import User
from jobplus.forms import UserProfile

user = Blueprint('user',__name__)



###Profile Config by EdwinYang2000
@user.route('/user/profile', methods=['GET','POST'])
@login_required     #role/employee decorators to be fixed later
def profile():
    user = current_user.user_detail
    form = UserProfile(obj=user)
    form.name.data = current_user.name
    form.email.data = current_user.email
    if form.validate_on_submit():
        form.updated_profile(current_user)
        flash('用户简历更新成功','success')
        return redirect(url_for('user.profile'))
    return render_template('profile.html',form=form,user=user)
