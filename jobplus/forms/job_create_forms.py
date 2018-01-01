from .base import *
from jobplus.models import db, User, Company, Job


#工作表
class JobForm(FlaskForm):
    name = StringField('工作名称', validators=[Required(),Length(2, 30)])
    wage = StringField('薪水', validators=[Required(),Length(3, 15)])
    location = StringField('工作地点',validators=[Required()])
    description = TextAreaField('工作描述', validators=[Required(), Length(10, 256)])
    requirement = TextAreaField('工作要求', validators=[Required(), Length(10, 256)])

    submit = SubmitField('提交')

    def create_job(self, company): #创建新工作
        job = Job()
        self.populate_obj(job)
        job.company_id = company.id
        db.session.add(job)
        db.session.commit()
        return job

    def edit_job(self, job): #编辑工作
        self.populate_obj(job)
        db.session.add(job)
        db.session.commit()
        return job