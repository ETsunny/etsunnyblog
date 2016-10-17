import time
import datetime
import json

from . import ModelMixin
from . import db


def format_time(timeStamp):
    dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
    otherStyleTime = dateArray.strftime("%B %d %Y")
    return otherStyleTime

class Blog(db.Model, ModelMixin):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    subtitle = db.Column(db.String())
    content = db.Column(db.String())
    simple = db.Column(db.String())
    created_time = db.Column(db.String())
    updated_time = db.Column(db.String())
    #
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, form):
        print('chest init', form)
        self.title = form.get('title', '')
        self.subtitle = form.get('subtitle', '')
        self.content = form.get('content', '')
        self.created_time = format_time(time.time())

    def update(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.subtitle = form.get('subtitle', '')
        self.updated_time = format_time(time.time())
        self.save()

    def json(self):
        d = {
            'id': self.id,
            'title': self.title,
            'simple': self.simple,
            'content': self.content,
            'created_time': self.created_time,
            'subtitle': self.subtitle,
        }
        return json.dumps(d, ensure_ascii=False)
