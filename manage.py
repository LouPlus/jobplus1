from jobplus.app import create_app


app = create_app('development')
app.config['SECRET_KEY'] = 'very very secret key'


if __name__ == '__main__':
    app.run()