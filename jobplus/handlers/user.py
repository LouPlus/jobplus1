from flask import Blueprint,render_template,flash,redirect,url_for
from flask import current_app,request
from flask_login import login_user,logout_user,login_required
from jobplus.models import User
from jobplus.forms import UserRegister

user = Blueprint('user',__name__)



###Profile Config by EdwinYang2000
@user.route('/user/profile/<int:user_id>',methods=['GET','POST'])
@login_required     #role/employee decorators to be fixed later
def profile(user_id):
    user = User.query.get_or_404(user_id)
    form = UserRegister(obj=user)
    if form.validate_on_submit():
        form.update_user(user)
        flash('用户简历更新成功','success')
        return redirect(url_for('user.profile'))
    return render_template('profile.html',form=form,user=user)
