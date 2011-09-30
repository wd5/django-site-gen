from flaskext.admin import Admin, ModelAdmin, AdminPanel

from app import app, db
from auth import auth
from models import User


admin = Admin(app, auth)

auth.register_admin(admin)