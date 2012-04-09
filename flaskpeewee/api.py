from flask_peewee.rest import RestAPI, RestResource, UserAuthentication, AdminAuthentication, APIKeyAuthentication

from app import app
from auth import auth
from models import User, APIKey


#user_auth = UserAuthentication(auth)
#admin_auth = AdminAuthentication(auth)

key_auth = APIKeyAuthentication(APIKey, protected_methods=['GET', 'POST', 'PUT', 'DELETE'])
key_auth_read_only = APIKeyAuthentication(APIKey, protected_methods=['POST', 'PUT', 'DELETE'])
api = RestAPI(app, default_auth=key_auth)


class UserResource(RestResource):
    exclude = ('password', 'email',)


api.register(User, UserResource)
