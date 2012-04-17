import datetime
import random
from hashlib import sha1

from flask_peewee.auth import BaseUser
from peewee import *

from app import app, db


class User(db.Model, BaseUser):
    username = CharField()
    password = CharField()
    email = CharField()
    join_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)

    def __unicode__(self):
        return self.username


class APIKey(db.Model):
    user = ForeignKeyField(User, unique=True)
    key = CharField()
    secret = CharField()

    def __unicode__(self):
        return '%s: %s' % (self.user.username, self.key)

    def create_key_secret(self):
        return (
            sha1('%s-%s' % (app.config['SECRET_KEY'], self.user.username).hexdigest()[:12],
            sha1('%s-%s' % (app.config['SECRET_KEY'], random.random())).hexdigest(),
        )

    def save(self):
        if not self.key:
            self.key, self.secret = self.create_key_secret()
        super(APIKey, self).save()
