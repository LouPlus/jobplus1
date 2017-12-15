from jobplus.app import create_app

<<<<<<< HEAD
#使用开发环境配置
app = create_app('development')
=======

app = create_app('development')
app.config['SECRET_KEY'] = 'very very secret key'

>>>>>>> manage requirement create

if __name__ == '__main__':
    app.run()