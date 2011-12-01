from flask import Flask

from flask_peewee.db import Database
from huey.queue import Invoker

from config import Configuration, QueueConfiguration


app = Flask(__name__)
app.config.from_object(Configuration)

db = Database(app)

invoker = Invoker(QueueConfiguration.QUEUE)
