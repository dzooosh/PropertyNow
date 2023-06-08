"""
`property` module
"""
from engine import storage
from typing import Dict, Any, Optional, List


class Property:
    """
    Abstraction layer for managing property-related operations.

    Attributes:
        storage (Storage): An instance of the Storage class for interacting with the database.
    """
    def __init__(self):
        """
        Initialize the Property class
        """
        self.__storage = storage

    def add_property(self, property_details: Dict[str, Any]) -> Dict[str, str]:
        """
        adds a new property

        args:
            property_details (dict): a dictionary with property details
        
        return:
            (str): 
        """
        if property_details is None or not isinstance(property_details, dict):
            return {'error': 'Invalid user credentials'}
        fields = property_details.keys()
        required_fields = [
           'title',
           'description',
           'price',
           'seller id',
           'location'
        ]
        missing_fields = [field for field in required_fields if field not in fields]
        if missing_fields:
            return {'error': f'Missing {", ".join(missing_fields)}'}
        if type(property_details['location']) is not dict:
            return {'error': 'location field is not a dictionary'}
        required_location_fields = [
           'city',
           'neighborhood'
        ]
        fields = property_details['location'].keys()
        missing_fields = [field for field in required_location_fields if field not in fields]
        if missing_fields:
            return {'error': f'Missing location fields: {", ".join(missing_fields)}'}
        seller = self.__storage.get_user(None, property_details['seller id'])
        if not seller:
            return {'error': "seller doesn't exist"}
        property_id = self.__storage.add_property(property_details)
        if property_id:
            return {'property id': property_id}
        else:
            return {'error': 'failed to add property'}

    def get_property(self, property_id: str) -> Dict[str, Any]:
        """
        retreives property by id

        args:
            property_id (str): id for the property
        
        return:
            property (dict): property linked with the property id
        """
        return self.__storage.get_property(property_id)

    def delete_property(self, property_id: str) -> bool:
        """
        deletes property

        args:
            property_id (str): id for the property

        return:
            (bool): result of the operation
        """
        return self.__storage.delete_property(property_id)

    def get_properties_for_seller(self, seller_id: str) -> List[Dict[str, Any]]:
        """
        returns all of the properties linked to a seller

        args:
            seller_id (str): user id for all of the properties to be deleted
        
        return:
            (list): list of all properties linked to a user
        """
        return self.__storage.get_properties_for_seller(seller_id)