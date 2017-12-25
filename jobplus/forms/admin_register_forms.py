from .base import *
from jobplus.models import db, User

class AdminRegister(FlaskForm):
    name = StringField('管理员名称', validators=[Required(), Length(2,24)])
    email = StringField('邮箱', validators=[Required(), Email(message='请输入合法email地址')])
    password = PasswordField('密码',validators=[Required()])
    repeat_password = PasswordField('重复密码',validators=[Required(),EqualTo('password')])
    image = StringField('头像链接')

    submit = SubmitField('提交')

    def create_user(self):
        user = User() #这里是添加企业用户的普通信息
        user.name = self.name.data
        user.email = self.email.data
        user.password = self.password.data
        user.logo_img = self.image.data
        user.role = 30 #管理员用户的权限是20
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')

class AdminProfile(FlaskForm):
    name = StringField('管理员名称', validators=[Required(), Length(2,24)])
    email = StringField('邮箱', validators=[Required(), Email(message='请输入合法email地址')])
    password = PasswordField('密码',validators=[Required()])
    repeat_password = PasswordField('重复密码',validators=[Required(),EqualTo('password')])
    image = StringField('头像链接')

    submit = SubmitField('提交')

    def updated_profile(self, user):
        #修改管理员用户信息
        user.name = self.name.data
        user.email = self.email.data
        user.password = self.password.data
        user.logo_img = self.image.data
        db.session.add(user)
        db.session.commit()
