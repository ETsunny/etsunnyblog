from models.blog import Blog
from models.user import User
from routes import *
from routes import blog

# for decorators
from functools import wraps

main = Blueprint('user', __name__)

UserModel = User
BlogModel = Blog


def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u


def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        print('admin required')
        u = current_user()
        if u is None:
            return redirect(url_for('.login_view'))
        return f(*args, **kwargs)
    return function


@main.route('/')
@admin_required
def index():
    ms = Blog.query.order_by(Blog.id.desc()).all()
    return render_template('usercenter.html', blogs=ms)


@main.route('/login')
def login_view():
    return render_template('login.html')


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User(form)
    # 检查 u 是否存在于数据库中并且 密码用户 都验证合格
    user = User.query.filter_by(username=u.username).first()
    if user is not None and user.validate_login(u):
        print('登录成功')
        session['user_id'] = user.id
        return redirect(url_for('.index'))
    else:
        print('登录失败')
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 user
    return redirect(url_for('.login_view'))

@main.route('/about')
def about_view():
    return render_template('about.html')
