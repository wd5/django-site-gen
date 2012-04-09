from flask_peewee.admin import Admin, ModelAdmin, AdminPanel

from app import app, db
from auth import auth
from models import User, APIKey


admin = Admin(app, auth)


class APIKeyPanel(AdminPanel):
    template_name = 'admin/panels/api_key.html'

    def get_context(self):
        users = User.select().join(
            APIKey, 'left outer'
        ).annotate(APIKey).having('count=0').order_by('username')
        return {
            'user_list': users
        }

    def get_urls(self):
        return (
            ('/apikey/provision/', self.provision),
        )

    def provision(self):
        if request.method == 'POST':
            if request.form.get('user'):
                key = APIKey.get_or_create(user_id=request.form['user'])
                flash('API Key created successfully')
        return redirect(self.dashboard_url())


auth.register_admin(admin)
admin.register(APIKey)
admin.register_panel('API Key provisioning', APIKeyPanel)
