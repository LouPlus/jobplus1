from .base import *
from jobplus.models import db, User, Company

class CompanyRegister(FlaskForm):
    name = StringField('企业名称', validators=[Required(), Length(2,24)])
    email = StringField('邮箱', validators=[Required(), Email(message='请输入合法email地址')])
    password = PasswordField('密码',validators=[Required()])
    repeat_password = PasswordField('重复密码',validators=[Required(),EqualTo('password')])
    image = StringField('头像链接')

    web = StringField('企业网站',validators=[Required()]) 
    oneword = StringField('一句话介绍',validators=[Required()])
    description = TextAreaField('企业介绍', validators=[Required(),Length(10,256)])

    submit = SubmitField('提交')

    def create_user(self):
        user = User() #这里是添加企业用户的普通信息
        user.name = self.name.data
        user.email = self.email.data
        user.password = self.password.data
        user.logo_img = self.image.data
        user.role = 20 #企业用户的权限是20
        db.session.add(user)
        new_user = User.query.filter_by(name=user.name).first()
        company = Company() #下面是添加企业用户的详细信息
        company.user = new_user
        company.website = self.web.data
        company.oneword = self.oneword.data
        company.description = self.description.data
        db.session.commit()
        return user

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')

class CompanyProfile(FlaskForm):
    name = StringField('企业名称', validators=[Required(), Length(2,24)])
    email = StringField('邮箱', validators=[Required(), Email(message='请输入合法email地址')])
    password = PasswordField('密码',validators=[Required()])
    repeat_password = PasswordField('重复密码',validators=[Required(),EqualTo('password')])
    image = StringField('头像链接')

    web = StringField('企业网站',validators=[Required()]) 
    oneword = StringField('一句话介绍',validators=[Required()])
    description = TextAreaField('企业介绍', validators=[Required(),Length(10,256)])

    submit = SubmitField('提交')

    def updated_profile(self,user):
        #修改企业用户信息
        user.name = self.name.data
        user.email = self.email.data
        user.password = self.password.data
        user.logo_img = self.image.data
        #下面是修改用户的详细信息
        company = user.company
        company.website = self.web.data
        company.oneword = self.location.data
        company.description = self.description.data
        db.session.add(user)
        db.session.add(company)
        db.session.commit()
