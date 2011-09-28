from hashlib import sha1
import datetime

from peewee import *

from app import db


class User(db.Model):
    username = CharField()
    password = CharField()
    email = CharField()
    join_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)

    def __unicode__(self):
        return self.username

    def set_password(self, password):
        self.password = sha1(password).hexdigest()
