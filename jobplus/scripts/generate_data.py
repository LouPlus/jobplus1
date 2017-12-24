from jobplus.models import db,User,Employee,Company,Job,Send

from datetime import datetime,date
import enum

#生成一个管理员,一个求职者,一个企业用户
def iter_users():
    #创建管理员
    yield User(
        name = 'admin',
        email = 'admin@163.com',
        password = '123456',
        logo_img = 'https://avatars3.githubusercontent.com/u/6779243?s=64&v=4',
        role = 30
    )
    #创建企业用户
    yield User(
        name = 'company',
        email = 'company@163.com',
        password = 'company',
        logo_img = 'https://avatars3.githubusercontent.com/u/6779243?s=64&v=4',
        role = 20
    )
    #创建求职者
    yield User(
        name = 'user',
        email = 'user@163.com',
        password = 'user',
        logo_img = 'https://avatars3.githubusercontent.com/u/6779243?s=64&v=4',
        role = 10
    )



# 生成求职者的信息
class SexType(enum.Enum):
    NONE = 0
    MALE = 1
    FEMALE = 2
    
def iter_employee():
    yield Employee(
        user = User.query.filter_by(name='user').first(),
        #sex = SexType.MALE,
        location = '北京',
        description = '大家好',
        resume = 'url'
    )

#生成企业的信息
def iter_company():
    yield Company(
        user = User.query.filter_by(name='company').first(),
        website = 'url',
        oneword = '这里是企业的介绍',
        description = '这是一家有着百年历史的企业｀'
    )

#生成职位表的信息
def iter_job():
    num = User.query.filter_by(name='company').first().id
    print(num)
    yield Job(
        name = '工程师',
        wage = '80万/年',
        location = '北京',
        company = Company.query.filter_by(user_id=num).first(),
        description = '我们需要招的是工程师',
        requirement = '我们需要有10年的工作经验'
    )

def iter_jobs():
    user = User.query.filter_by(name='user').first()
    with open(os.path.join(os.path.dirname(__file__),'../..','data','job.json')) as f:
        jobs = json.load(f)
    for job in jobs:
        yield Job(
            name = job['name'],
            location = job['location'],
            wage = job['wage'],
            # description = job['description'],
            # qualifications = job['qualifications'],
            # experience = job['experience'],
            # work_time = job['work_time']
        )


#生成投递表
class Qualify_Type(enum.Enum):
    UNREAD = 0 #未被阅读
    READ = 1 #已被阅读
    REFUSE = 2 #拒绝该简历
    ACCEPT = 3 #接受该简历

def iter_send():
    num = User.query.filter_by(name='company').first().id
    company_id = Company.query.filter_by(user_id=num).first()
    yield Send(
        company_id = company_id.id,
        #投递的工作需要根据职位和公司id确定
        job_id = Job.query.filter_by(name='工程师',company_id=company_id.id).first().id,
        employee_id = Employee.query.filter_by(user_id = User.query.filter_by(name='user').first().id).first().id,
        qualify = 'UNREAD'
    )


def run():
    for user in iter_users():
        db.session.add(user)

    for employee in iter_employee():
        db.session.add(employee)

    for company in iter_company():
        db.session.add(company)

    for job in iter_job():
        db.session.add(job)

    for send in iter_send():
        db.session.add(send)

    try:
        db.session.commit()        
    except Exception as e:
        print('------------')
        print(e)
        db.session.rollback()

