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

    def create_job(self, user): #创建新工作
        job = Job()
        self.populate_obj(job)
        job.company_id = user.company.id
        db.session.add(job)
        db.session.commit()
        return job

    def edit_job(self, job_id): #编辑工作
        job = Job.query.filter_by(id=job_id).first()
        self.populate_obj(job)
        db.session.add(job)
        db.session.commit()
        return job