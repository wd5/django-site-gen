from flask import Flask

from flaskext.db import Database


app = Flask(__name__)
app.config.from_object('config.Configuration')

db = Database(app)
