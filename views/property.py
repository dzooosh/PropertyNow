"""
a view for `Prtoperty` objects that handles all default REST API
actions
"""

from flask import request, jsonify, url_for, send_file, send_from_directory
from views import property_views
from models.property import Property

propertyClass = Property()

@property_views.route('/images/<string:filename>', methods=['GET'], strict_slashes=False)
def get_image(filename):
    """
    return property image
    """
    try:
        return send_from_directory(property_views.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        return jsonify({'error': 'not found'})

@property_views.route('/', methods=['GET'], strict_slashes=False)
def get_properties():
    """
    returns a list of properties from the database
    """
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('limit', default=20, type=int)
    properties = propertyClass.get_properties(page - 1, page_size)
    if properties is None:
        return jsonify({'error': 'Failed to retreive properties'}), 500
    for property in properties:
        property['_id'] = str(property['_id'])
        property['image_url'] = property['image_url'][0]
    return jsonify(properties)

@property_views.route('/<string:property_id>', methods=['GET'], strict_slashes=False)
def get_property(property_id):
    """
    retrieve property using property id
    """
    property = propertyClass.get_property(property_id)
    if not property:
        return jsonify({'error': 'not found'}), 404
    property['image_url'] = property['image_url'][1]
    return jsonify(property)

@property_views.route('/locations', methods=['GET'], strict_slashes=False)
def get_locations():
    """
    retreive locations
    """
    return jsonify(propertyClass.get_locations())
