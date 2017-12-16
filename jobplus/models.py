# -*- coding: utf-8 -*-

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_migrate import Migrate

"""临时测试用"""
"""
from flask import Flask, render_template
app = Flask(__name__)
app.config.update(dict(SECRET_KEY = 'very secret key',
                       SQLALCHEMY_DATABASE_URI='mysql+mysqldb://root@localhost:3306/jobweb?charset=utf8'))
db = SQLAlchemy(app)
"""
"""临时测试用"""


db = SQLALchemy()

class Base(db.Model):
    """时间戳基类"""
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base):
    __tablename__ = 'user'

    ROLE_EMPLOYEE = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.SmallInteger, default=ROLE_EMPLOYEE)
    name = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    logo_img = db.Column(db.String(128))
    #company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company_id = db.relationship('Company', uselist=False)
    #employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    employee = db.relationship('Employee', uselist=False)

    def __repr__(self):
        return '<User:{}>'.format(self.name)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password_hash(self, password):
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

class Employee(Base):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False)
    sex = db.Column(db.Enum(SexType), default=SexType.NONE)
    location = db.Column(db.String(64))
    description = db.Column(db.String(256))
    resume = db.Column(db.String(128))

class Company(Base):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False)
    website = db.Column(db.String(128))
    oneword = db.Column(db.String(64))
    description = db.Column(db.String(256))

class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    wage = db.Column(db.String(64))
    location = db.Column(db.String(64))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete = 'CASCADE'))
    company = db.relationship('Company')
    description = db.Column(db.String(64))
    requirement = db.Column(db.String(64))

class Qualify_Type(enum.Enum):
    UNREAD = 0
    READ = 1
    REFUSE = 2
    UNREFUSE = 3

class Send(Base):
    __tablename__ = 'send'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    resume = db.relationship('Employee')
    qualify = db.Column(db.Enum(Qualify_Type), default = Qualify_Type.UNREAD)

"""临时测试用"""
"""
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
"""
"""临时测试用"""
