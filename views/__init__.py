from flask import Blueprint

property_views = Blueprint("property_views", __name__)
admin = Blueprint("admin", __name__, url_prefix="/admin")
auth_views = Blueprint("auth_views", __name__, url_prefix="/auth")

from views.property import *
from views.auth import *
from views.admin import *