from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from models import db
# 这里 import 具体的 Model 类是为了给 migrate 用
# 如果不 import 那么无法迁移
# 这是 SQLAlchemy 的机制
from models.user import User
from models.blog import Blog

from routes.blog import main as routes_blog
from routes import main as routes
from routes.user import main as routes_user

# from routes.admin_views import admin
# from routes.chest_views import chest
# from routes.question_views import question
# from routes.topic_views import topic

app = Flask(__name__)
db_path = 'blog.sqlite'
manager = Manager(app)


def register_routes(app):
    app.register_blueprint(routes_blog, url_prefix='/blog')
    app.register_blueprint(routes_user, url_prefix='/blog/user')
    app.register_blueprint(routes)



def configure_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = 'secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    db.init_app(app)
    register_routes(app)


def configured_app():
    configure_app()
    return app


# 自定义的命令行命令用来运行服务器
@manager.command
def server():
    # app = configured_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=3000,
    )
    app.run(**config)


def configure_manager():
    """
    这个函数用来配置命令行选项
    """
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    configure_manager()
    configure_app()
    manager.run()
