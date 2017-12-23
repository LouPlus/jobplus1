from .base import *
from jobplus.models import db, User, Employee


#Profile表 # by EdwinYang2000
class UserProfile(FlaskForm):
    name = StringField('求职者姓名', validators=[Required(), Length(4,24)])
    email = StringField('邮箱', validators=[Required(), Email(message='请输入合法email地址')])
    password = PasswordField('密码')
    submit = SubmitField('提交')
    #sex = StringField('性别')
    location = StringField('城市')
    description = StringField('自我介绍', validators=[Required(), Length(10, 256)])
    resume = StringField('简历地址')
    submit = SubmitField('提交')


    def updated_profile(self, user):
        user.name = self.name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data

        if user.user_detail:
            user_detail = user.user_detail

        else:
            user_detail = Employee()
            user_detail.user_id = user.id
        self.populate_obj(user_detail)
        db.session.add(user)
        db.session.add(user_detail)
        db.session.commit()