# jobplus1
LouPlus Team 1 https://www.shiyanlou.com/louplus/python

## Contributors

* [louplus](https://github.com/louplus)
* [edwinymc@icloud.com](https://github.com/EdwinYang2000)
* [goff_lin](https://github.com/Wooding-wood)
* [会飞的鳄鱼](https://github.com/luoyuedong)
* [WMN7](https://github.com/wmn7)

## 使用sql文件初始化数据库

在主目录下有一个jobplus.sql文件，下面导入这个sql文件


1. mysql -u root -p  进入数据库
2. CREATE DATABASE jobplus;创建数据库 
3. use jobplus; 切换数据库
4. source /所在路径/jobplus.sql;导入数据库文件  


参考资料:http://blog.csdn.net/piaocoder/article/details/51995372


## 初始化数据库

在本地创建数据库 create database jobplus
接着修改config.py里的SQLALCHEMY_DATABASE_URI

下面初始化数据库

```
$ FLASK_APP=manage.py flask db init
$ FLASK_APP=manage.py flask db migrate -m 'init database'
$ FLASK_APP=manage.py flask db upgrade

$ FLASK_APP=manage.py flask shell
$ from jobplus.scripts import run
$ run()
```

### 初始化的成员
- 管理员


1. name = admin
2. email = admin@163.com
3. password = 123456

- 企业用户

1. name = company
2. email = company@163.com
3. password = company

- 招聘用户

1. name = user
2. email = user@163.com
3. password = user
