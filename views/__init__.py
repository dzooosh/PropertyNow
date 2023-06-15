from flask import Blueprint

property_views = Blueprint("property_views", __name__, url_prefix="/property")

from views.property import *