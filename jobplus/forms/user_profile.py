from .base import *
from jobplus.models import db, User, Employee,Company


#UserProfile表 修改普通用户的信息
class UserProfile(FlaskForm):
    name = StringField('求职者姓名', validators=[Required(), Length(4,24)])
    email = StringField('邮箱', validators=[Required(), Email(message='请输入合法email地址')])
    password = PasswordField('密码')
    submit = SubmitField('提交')
    sex = SelectField('性别',validators=[Required()] , choices=[('MALE', '男性'),('FEMALE', '女性'),('NULL', '保密')]) 
    location = StringField('城市')
    description = TextAreaField('自我介绍', validators=[Required(), Length(10, 256)])
    resume = StringField('简历地址')
    submit = SubmitField('提交')


    def updated_profile(self, user):
        #修改用户信息
        user.name = self.name.data
        user.email = self.email.data
        user.password = self.password.data
        user.logo_img = self.image.data
        db.session.add(user)
        #下面是修改用户的详细信息
        employee = user.employee
        employee.sex = self.sex.data
        employee.location = self.location.data
        employee.description = self.description.data
        employee.resume = self.resume.data
        db.session.add(employee)
        db.session.commit()

#CompanyProfile表 修改企业用户的信息
class ComapnyProfile(FlaskForm):
    name = StringField('企业名称', validators=[Required(), Length(2,24)])
    email = StringField('邮箱', validators=[Required(), Email(message='请输入合法email地址')])
    password = PasswordField('密码',validators=[Required()])
    repeat_password = PasswordField('重复密码',validators=[Required(),EqualTo('password')])
    image = StringField('头像链接')

    web = StringField('企业网站',validators=[Required()]) 
    oneword = StringField('一句话介绍',validators=[Required()])
    description = TextAreaField('企业介绍', validators=[Required(),Length(10,256)])

    def updated_profile(self, company):
        company.name = self.name.data
        company.email = self.email.data
        if self.password.data:
            company.password = self.password.data

        if company.user_detail:
            user_detail = company.user_detail

        else:
            user_detail = Employee()
            user_detail.user_id = company.id
        self.populate_obj(user_detail)
        db.session.add(company)
        db.session.add(user_detail)
        db.session.commit()