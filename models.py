#！ -*-coding:utf-8 -*-
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate = datetime.utcnow)


class User(Base, UserMixin):
    __tablename__ = 'user'

    ROLE_USER = 10 #求职者权限
    ROLE_COMPANY = 20 #企业用户权限
    ROLE_ADMIN = 30 #管理员权限

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32),unique=True, index=True, nullable=False)
    email = db.Column(db.String(64),unique=True, index=True, nullable=False)
    _password = db.Column('password',db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)#权限
    employed_info = db.relationship('Employed')
    company_info = db.relationship('Company')

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self,password):

        return check_password_hash(self._password,password)

    @property
    def is_user(self):
        return self.role == self.ROLE_USER

    @property
    def is_user(self):
        return self.role == self.ROLE_COMPANY

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN


class Employed(Base):

    __tablename__ = 'employed'

    id = db.Column(db.Integer, primary_key=True)
    sex = db.Column(db.String(32))
    location = db.Column(db.String(64))
    detail = db.Column(db.String(256))
    resume = db.Column(db.String(128)) #resume_url,有时间再做前端上传文件？？


class Company(Base):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),unique=True, index=True, nullable=False)#企业名称
    logo_img = db.Column(db.String(256)) #企业logo
    website = db.Column(db.String(64)) #企业网站
    location = db.Column(db.String(64)) #企业地点
    oneword = db.Column(db.String(128)) #企业一句话简介
    detail = db.Column(db.String(256)) #企业详细介绍


class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64)) #职位名称
    wage = db.Column(db.String(64)) #薪资
    location = db.Column(db.String(64))  #工作地点
    detail = db.Column(db.String(128)) #工作描述
    exp = db.Column(db.String(32)) #经验
    company_info = db.Column(db.String(128))#企业地点


class Send(Base):

    __tablename__ = 'send'

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(db.String, db.ForeignKey('company.id', ondelete='SET NULL'))
    company = db.relationship('Company',uselist=False)

    user_id = db.Column(db.String, db.ForeignKey('user.id', ondelete='SET NULL'))
    user = db.relationship('User', uselist=False)

    job_id = db.Column(db.String, db.ForeignKey('job.id', ondelete='SET NULL'))
    job = db.relationship('Job',uselist=False)

    qualify = db.Column(db.String(32))


    def __repr__(self):
        return '<Send:{}>'.format(self.name)

