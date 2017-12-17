# jobplus1
LouPlus Team 1 https://www.shiyanlou.com/louplus/python

## Contributors

* [louplus](https://github.com/louplus)
* [edwinymc@icloud.com](https://github.com/EdwinYang2000)
* [goff_lin](https://github.com/Wooding-wood)
* [会飞的鳄鱼](https://github.com/luoyuedong)
* [WMN7](https://github.com/wmn7)

## 初始化数据库

在本地创建数据库 create database jobplus
接着修改config.py里的SQLALCHEMY_DATABASE_URI

下面初始化数据库

$ FLASK_APP=manage.py flask db init
$ FLASK_APP=manage.py flask db migrate -m 'init database'
$ FLASK_APP=manage.py flask db upgrade

$ FLASK_APP=manage.py flask shell
$ from jobplus.scripts import run
$ run()

### 初始化的成员
- 管理员


name = admin
email = admin@163.com
password = 123456

- 企业用户

name = company
email = company@163.com
password = company

- 招聘用户

name = user
email = user@163.com
password = user
