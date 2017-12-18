# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_migrate import Migrate
from datetime import datetime

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                        default=datetime.utcnow,
                        onupdate=datetime.utcnow)


class User(Base,UserMixin):
    __tablename__ = 'user'

    ROLE_EMPLOYEE = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    #这里存logo_img的url
    logo_img = db.Column(db.String(128))
    #连接到公司的关系1-1关系
    company = db.relationship('Company', uselist=False)
    #连接到求职者关系1-1关系
    employee = db.relationship('Employee', uselist=False)
    #用户权限
    role = db.Column(db.SmallInteger, default=ROLE_EMPLOYEE)

    def __repr__(self):
        return '<User:{}>'.format(self.name)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password_hash(self, password):
        """判断用户输入的密码和存储的hash密码是否相等
        """
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY

    @property
    def is_emploee(self):
        return self.role == self.ROLE_EMPLOYEE


import enum
class SexType(enum.Enum):
    NONE = 0
    MALE = 1
    FEMALE = 2

#求职者表
class Employee(Base):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False)

    sex = db.Column(db.Enum(SexType), default=SexType.NONE)
    location = db.Column(db.String(64))
    description = db.Column(db.String(256))
    resume = db.Column(db.String(128))

#企业表
class Company(Base):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),index=True)
    user = db.relationship('User', uselist=False)

    website = db.Column(db.String(128))
    oneword = db.Column(db.String(64))
    description = db.Column(db.String(256))

#职位表
class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64)) #不同公司可以有一样名字的职位
    wage = db.Column(db.String(64))
    location = db.Column(db.String(64))

    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete = 'CASCADE'))
    company = db.relationship('Company',uselist=False)

    description = db.Column(db.String(256))
    requirement = db.Column(db.String(256))

class Qualify_Type(enum.Enum):
    UNREAD = 0 #未被阅读
    READ = 1 #已被阅读
    REFUSE = 2 #拒绝该简历
    ACCEPT = 3 #接受该简历

#投递表
class Send(Base):
    __tablename__ = 'send'

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

    resume = db.relationship('Employee')

    qualify = db.Column(db.Enum(Qualify_Type), default = Qualify_Type.UNREAD)

