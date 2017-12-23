from .base import *
from jobplus.models import db, User


#Profile表 # by EdwinYang2000
# edit wmn7
class UserRegister(FlaskForm):
    name = StringField('求职者姓名', validators=[Required(), Length(4,24)])
    email = StringField('邮箱', validators=[Required(), Email(message='请输入合法email地址')])
    password = PasswordField('密码',validators=[Required()])
    repeat_password = PasswordField('重复密码',validators=[Required(),EqualTo('password')])
    image = StringField('头像链接')

    sex = StringField('性别',validators=[Required()])
    location = StringField('城市',validators=[Required()])
    description = StringField('自我介绍', validators=[Required(),Length(10,256)])
    resume = StringField('简历地址')

    submit = SubmitField('提交')

    def create_user(self):
        user = User()
        user.name = self.name.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')


    def create_user(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user