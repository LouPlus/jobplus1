from .base import *
from jobplus.models import db, User


#Profile表 # by EdwinYang2000
class UserProfile(FlaskForm):
    name = StringField('求职者姓名', validators=[Required(), Length(4,24)])
    email = StringField('邮箱', validators=[Required(), Email(message='请输入合法email地址')])
    password = PasswordField('密码')
    sex = StringField('性别')
    location = StringField('城市')
    description = StringField('自我介绍', validators=[Required(),Length(10,256)])
    resume = StringField('简历地址')
    submit = SubmitField('提交')


    def validate_name(self,field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('求职者姓名已经存在')


    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')


    def update_user(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user
