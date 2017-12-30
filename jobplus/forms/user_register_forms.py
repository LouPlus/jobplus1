from .base import *
from jobplus.models import db, User, Employee
from flask import current_app

#Profile表 # by EdwinYang2000
# edit wmn7
class UserRegister(FlaskForm):
    name = StringField('求职者姓名', validators=[Required(), Length(2,24)])
    email = StringField('邮箱', validators=[Required(), Email(message='请输入合法email地址')])
    password = PasswordField('密码',validators=[Required()])
    repeat_password = PasswordField('重复密码',validators=[Required(),EqualTo('password')])
    image = StringField('头像链接')

    sex = SelectField('性别',validators=[Required()] , choices=[('MALE', '男性'),('FEMALE', '女性'),('NONE', '保密')]) 
    location = StringField('城市',validators=[Required()])
    description = TextAreaField('自我介绍', validators=[Required(),Length(10,256)])
    resume = StringField('简历地址')

    submit = SubmitField('提交')

    def create_user(self): #创建用户
        user = User() #这里是添加用户的普通信息
        user.name = self.name.data
        user.email = self.email.data
        user.password = self.password.data
        user.logo_img = self.image.data
        db.session.add(user)
        new_user = User.query.filter_by(name=user.name).first()
        employee = Employee() #下面是添加用户的详细信息
        employee.user = new_user
        employee.sex = self.sex.data
        employee.location = self.location.data
        employee.description = self.description.data
        employee.resume = self.resume.data
        db.session.add(employee)
        db.session.commit()
        return user

    def validate_name(self,field): #update
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('用户名已经存在')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')

class UserProfile(FlaskForm):
    name = StringField('求职者姓名', validators=[Required(), Length(2,24)])
    email = StringField('邮箱', validators=[Required(), Email(message='请输入合法email地址')])
    password = PasswordField('密码',validators=[Required()])
    repeat_password = PasswordField('重复密码',validators=[Required(),EqualTo('password')])
    image = StringField('头像链接')

    sex = SelectField('性别',validators=[Required()],choices=[('MALE', '男性'),('FEMALE', '女性'),('NONE', '保密')]) 
    location = StringField('城市',validators=[Required()])
    description = TextAreaField('自我介绍', validators=[Required(),Length(10,256)])
    resume = StringField('简历地址')

    submit = SubmitField('提交')

    def updated_profile(self,user):#更新用户信息
        #修改用户信息
        user.name = self.name.data
        user.email = self.email.data
        user.password = self.password.data
        user.logo_img = self.image.data
        #下面是修改用户的详细信息
        employee = user.employee
        employee.sex = self.sex.data
        employee.location = self.location.data
        #employee.location = 'beijin11'
        employee.description = self.description.data
        employee.resume = self.resume.data

        current_app.logger.debug('self.location.data : '+self.location.data)
        current_app.logger.debug('employee.location : '+employee.location)

        db.session.add(user)
        db.session.add(employee)
        db.session.commit()
