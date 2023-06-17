"""
a view for `admin` that handles all admins REST API
actions
Admin - Add (user, admin, properties)
        Remove (user, properties)
        Update(properties, User (change user to admin))
"""
from views import admin


@admin.route('/')
def admin_home():
    return "Welcome To Admin Home"