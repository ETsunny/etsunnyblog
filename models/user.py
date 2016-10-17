import time
import json

from . import ModelMixin
from . import db


class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    avatar = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    # has relationship with blog
    blogs = db.relationship('Blog', backref="user")

    def __init__(self, form):
        print('chest init', form)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.created_time = int(time.time())

    def validate_login(self, u):
        return u.username == self.username and u.password == self.password

    def update(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.avatar = form.get('avatar', '')
        self.save()

    def json(self):
        d = {
            'id': self.id,
            'username': self.title,
            'created_time': self.created_time,
        }
        return json.dumps(d, ensure_ascii=False)
