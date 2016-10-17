import datetime
from models.blog import Blog
from models.user import User
from routes import *

# for decorators
from functools import wraps

main = Blueprint('blog', __name__)

Model = Blog


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
def index():
    ms = Blog.query.order_by(Blog.id.desc()).all()

    return render_template('index.html', blogs=ms)


@main.route('/detail/<int:id>')
def detail(id):
    b = Model.query.get(id)
    return render_template('detail.html', blog=b)


@main.route('/add', methods=['GET'])
@admin_required
def add_view():
    return render_template('edit.html')


@main.route('/add', methods=['POST'])
@admin_required
def add():
    form = request.form
    m = Model(form)
    m.save()
    return redirect(url_for('user.index'))


@main.route('/update/<int:id>', methods=['GET'])
@admin_required
def update_view(id):
    b = Model.query.get(id)
    return render_template('update_blog.html', blog=b)


@main.route('/update/<int:id>', methods=['POST'])
@admin_required
def update(id):
    form = request.form
    t = Model.query.get(id)
    t.update(form)
    return redirect(url_for('user.index'))


@main.route('/delete/<int:id>')
@admin_required
def delete(id):
    t = Model.query.get(id)
    t.delete()
    return redirect(url_for('user.index'))



@main.route('/archives')
def archives_view():
        ms = Blog.query.order_by(Blog.id.desc()).all()
        return render_template('archives.html', blogs=ms)
