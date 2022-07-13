from flask import session, url_for, redirect, flash
from flask_admin.contrib.sqla import ModelView


# Override Flask_Admin ModelView methods (is_accessible and inaccessible_callback)
class AgrihandyAdmin(ModelView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    def is_accessible(self):
        return session.get('username') == "Admin"

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            flash ('Permission not granted. Only Administrators can view AgriHandy Admin.','danger')
            return redirect(url_for('main.index'))




