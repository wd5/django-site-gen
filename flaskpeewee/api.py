from flaskext.rest import RestAPI, RestResource, UserAuthentication, AdminAuthentication

from app import app
from auth import auth
from models import User


user_auth = UserAuthentication(auth)
admin_auth = AdminAuthentication(auth)

api = RestAPI(app, default_auth=user_auth)


class UserResource(RestResource):
    exclude = ('password', 'email',)


api.register(User, UserResource, auth=admin_auth)
