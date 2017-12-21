from .base import *

from jobplus.models import User

#登录界面的表格
class LoginForm(FlaskForm):
    name = StringField('用户名',validators=[Required(),Length(3,24)])
    password = PasswordField('密码',validators=[Required(),Length(3,26)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_name(self,field):
        if field.data and not User.query.filter_by(name=field.data).first():
            raise ValidationError('用户名未注册')
    
    def validate_password(self,field):
        user = User.query.filter_by(name=self.name.data).first()
        if user and not user.check_password_hash(field.data):
            raise ValidationError('密码错误')