"""
a view for `Prtoperty` objects that handles all default REST API
actions
"""

from flask import request, jsonify, url_for, send_file
from views import property_views
from models.property import Property

propertyClass = Property()

@property_views.route('/images/<string:filename>', methods=['GET'], strict_slashes=False)
def get_image(filename):
    """
    return property image
    """
    image_path = f'property_images/{filename}'
    return send_file(image_path, mimetype='image/png')

@property_views.route('/', methods=['GET'], strict_slashes=False)
def get_properties():
    """
    returns a list of properties from the database
    """
    page = request.args.get('page', default=0, type=int)
    page_size = request.args.get('limit', default=20, type=int)
    properties = propertyClass.get_properties(page, page_size)
    if properties is None:
        return jsonify({'error': 'Failed to retreive properties'}), 500
    for property in properties:
        property['_id'] = str(property['_id'])
        property['image_url'] = f'http://localhost:5000/properties/images/{property.get("_id")}.png'
        print(property['image_url'])
    return jsonify(properties), 200

@property_views.route('/<string:property_id>', methods=['GET'], strict_slashes=False)
def get_property(property_id):
    """
    retrieve property using property id
    """
    property = propertyClass.get_property(property_id)
    if not property:
        return jsonify({})
    property['_id'] = str(property['_id'])
    return jsonify(property)

