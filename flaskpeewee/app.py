from flask import Flask

from flaskext.db import Database
from skew.queue import Invoker

from config import Configuration, QueueConfiguration


app = Flask(__name__)
app.config.from_object(Configuration)

db = Database(app)

invoker = Invoker(QueueConfiguration.QUEUE)
