from pathlib import Path
from abc import ABC, abstractproperty
import functools

from tinydb import TinyDB, where

from .persistent import Persistent

class Database(object):
    
    def __init__(self, project_path):
        self.db = TinyDB(str(Path(project_path, "driftai.db")))

    def __getattr__(self, name):
        return getattr(self.db, name)


class BaseCollection(ABC):

    def __init__(self, **kwargs):
        self.collection = kwargs["db"].table(self.collection_name)

    def get(self, id_):
        """
        Return a record given its id

        Parameters
        ----------
        id_: str
            Record unique identifier

        Returns
        -------
        driftai.db.Persistent

        """
        data = self.collection.get(where("id") == id_)
        return self.persistent.load_from_data(data) if data else None

    def list_ids(self):
        """
        List all ids of a collection

        Returns
        -------
        list of str
            List of ids
        """
        return [ r["id"] for r in self.collection.all() ]

    @abstractproperty
    def collection_name(self):
        pass

    @abstractproperty
    def persistent(self):
        pass

    def save(self, instance):
        """
        Store a persistent instance to driftai db

        Parameters
        ----------
        instance: driftai.db.Persistent
            Instance to be stored

        """
        if not isinstance(instance, Persistent):
            raise TypeError("instance must be of Persistent type")

        self.collection.insert(instance.get_info())

    def update(self, instance):
        """
        Update a persistent instance to driftai db

        Parameters
        ----------
        instance: driftai.db.Persistent
            Instance to be updated
        """
        if not isinstance(instance, Persistent):
            raise TypeError("instance must be of Persistent type")
        self.collection.update(instance.get_info(), where("id") == instance.id)

    def exists(self, id_):
        """
        Checks if an instance with an specific id exists

        Parameters
        ----------
        id: str
            Record unique identifier

        Returns
        -------
        boolean
            Instance with id exists?
        """
        return self.collection.get(where("id") == id_) is not None

    def __getattr__(self, name):
        """Calls the attribure of tinydb.Table"""
        return getattr(self.collection, name)

class ApproachCollection(BaseCollection):

    @property
    def collection_name(self):
        return "approaches"

    @property
    def persistent(self):
        from driftai import Approach
        return Approach

class DatasetCollection(BaseCollection):

    @property
    def collection_name(self):
        return "datasets"

    @property
    def persistent(self):
        from driftai.data import Dataset
        return Dataset


class SubDatasetCollection(BaseCollection):

    @property
    def collection_name(self):
        return "subdatasets"

    @property
    def persistent(self):
        from driftai.data import SubDataset
        return SubDataset

class RunsCollection(BaseCollection):

    def __init__(self, approach_id, **kwargs):
        super().__init__(**kwargs)
        self.approach_id = approach_id

    @property
    def collection_name(self):
        return "approaches"

    @property
    def persistent(self):
        from driftai.run import Run
        return Run

    def get(self, id_):
        approach = self.collection.get(where("id") == self.approach_id)
        possible_result =  list(filter(lambda r: r["id"] == id_, approach["runs"]))
        return self.persistent.load_from_data(possible_result[0]) if possible_result else None

    def save(self, instance):
        from driftai.run import Run
        if not isinstance(instance, Run):
            raise TypeError("instance must be of Run type")

        self.collection.update(append_to("runs", instance.get_info()), where("id") == self.approach_id)

    def update(self, instance):
        from driftai.run import Run
        if not isinstance(instance, Run):
            raise TypeError("instance must be of Run type")
        
        self.collection.update(update_collection_item("runs", instance.get_info()), where("id") == self.approach_id)


    
def append_to(collection, item):
    """Appends a new item to a list inside a document"""
    def transform(doc):
        doc[collection].append(item)
        
    return transform


def update_collection_item(collection, item):
    def transform(doc):
        items = doc[collection] 
        for i in range(len(items)):
            if items[i]["id"] == item["id"]:
                items[i] = item
                return
    return transform

# TODO: Global config
_global_config = {
    'db': None,
    'project_path': '.'
}

class DatabaseInjector(object):

    @staticmethod
    def db():
        db = _global_config.get('db')
        if not db:
            _global_config['db'] = Database(_global_config.get('project_path'))
        return  _global_config['db']
    
    @staticmethod
    def reset(): 
        db = _global_config.get('db')
        if db:
            db.close()
            _global_config['db'] = None
    
class Collections(object):

    def approaches():
        return ApproachCollection(db=DatabaseInjector.db())

    def datasets():
        return DatasetCollection(db=DatabaseInjector.db())
    
    def subdatasets():
        return SubDatasetCollection(db=DatabaseInjector.db())

    def runs(approach_id):
        return RunsCollection(approach_id, db=DatabaseInjector.db())

        
def set_project_path(path):
    """
    Set the project which you are working on. 
    This will change the path where driftai will look for the embedded database

    Parameters
    ----------
    path: str
        DriftAI's project path
    """
    _global_config['project_path'] = path
