from pathlib import Path
from abc import ABC, abstractmethod

from optapp.exceptions import OptAppProjectLoadPathIsNotDirException


class Persistent(ABC):
    """
    Provides serialization to tinydb.
    """
    def save(self):
        """
        Save a class instance to TinyDB
        """
        self.collection().save(self)

    def update(self):
        """
        Updates a class instance to TinyDB
        """
        self.collection().update(self)

    @abstractmethod
    def get_info(self):
        """
        Generate essential information

        Returns
        -------
        dict
            Contain essential data to serialize the class instance
        """
        pass

    @staticmethod
    @abstractmethod
    def collection():
        """
        Returns the collection where persistent object should be stored

        Returns
        -------
        class BaseCollection
            Class representing the table where the object will be stored
        """
        pass

    @property
    @abstractmethod
    def id(self):
        """
        Get the unique identifier of the Persistent instance

        Returns
        -------
        str
            Unique identifier
        """
        pass


    @classmethod
    def load(cls, id_):
        """
        Creates an instance of the cls class using the unique identifier

        Parameters
        ----------
        id: str
            Unique identifier of the persistent instance

        Returns
        -------
        Persistent
            Instance created using JSON data comming from tinydb 
        """
        return cls.collection().get(id_)

    @classmethod
    @abstractmethod
    def load_from_data(cls, data):
        """
        Creates an instance of the cls class using data comming from tinydb

        Parameters
        ----------
        data: dict
            Dict containing the JSON data coming from TinyDB

        Returns
        -------
        Persistent
            Instance created using JSON data comming from tinydb 
        """
        pass

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            info1 = self.get_info()
            info2 = other.get_info()
            for k in info1.keys():
                if info1[k] != info2[k]:
                    return False
            return True
        return False

    def __ne__(self, other):
        return not (self == other)
