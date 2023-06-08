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

    def add_property(self, property_details: Dict[str, Any]) -> str:
        """
        adds a new property

        args:
            property_details (dict): a dictionary with property details
        
        return:
            (str): 
        """
        return self.__storage.add_property(property_details)

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