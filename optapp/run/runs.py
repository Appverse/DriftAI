import warnings
from datetime import datetime
import hashlib
from pathlib import Path
from collections import OrderedDict
import itertools
import re

from optapp.data import SubDataset
from optapp.db import Persistent
from optapp.utils import str_to_date

from optapp.exceptions import OptAppRunFileDoesNotExistException, \
                              OptAppRunFileWrongStructureException, \
                              OptAppInstanceExistsException

class Run(Persistent):
    def __init__(self, approach_id, subdataset, subdataset_set, run_parameters, 
                    creation_date=None, submitted_date=None, finish_date=None, 
                    results=None, status="waiting", id=None):

        self.approach_id = approach_id
        self.subdataset = subdataset
        self.run_parameters = run_parameters
        self._status = status
        self._results = results
        self.creation_date = str_to_date(creation_date) or datetime.now()
        self.sumbission_date = submitted_date
        self.finish_date = finish_date
        self.subdataset_set = subdataset_set
        self._id = id or self._get_id()
        if creation_date is None and Run.collection(self.approach_id).exists(self.id):
            raise OptAppInstanceExistsException("Run")


    @property
    def id(self):
        return self._id
    
    @staticmethod
    def collection(approach_id):
        """
        Get table containing runs

        Returns
        -------
        TinyDB instance
        """
        from optapp.db import Collections
        return Collections.runs(approach_id)

    @classmethod
    def load_from_data(cls, data, **kwargs):
        """
        Loads a Run from the data coming from TinyDB

        Parameters
        ----------
        data: dict
            Dict containing the JSON data

        Raises
        ------
        OptAppSubDatasetInfoFileWrongStructureException
            If data has worng keys

        Returns
        -------
        optapp.Run
            New Run instance
        """
        from optapp.result_report import Result

        def check_run_file_structure(params):
            if not isinstance(params, dict):
                return False
            dict_contents = {
                "approach_id", "subdataset", "subdataset_set", 
                "run_parameters", "status", "results", "submitted_date",
                "finish_date", "creation_date", "id"
            }
            return dict_contents.intersection(list(params.keys())) == dict_contents
        
        if check_run_file_structure(data):
            data["subdataset"] = kwargs.get('subdataset') or SubDataset.collection().get(data["subdataset"])
            data["results"] = Result(**data["results"]) if data["results"] else None
            return cls(**data)
        else:
            raise OptAppRunFileWrongStructureException()

    def _get_id(self):
        pars = str(self.run_parameters)
        pars_hash = hashlib.md5(pars.encode('utf-8')).hexdigest()
        return "{}_{}_{}".format(self.approach_id, self.subdataset_set, pars_hash)

    def get_train_data(self):
        """
        Get the train data from the run related subdataset set

        Returns
        -------
        dict
            Containing records and its labels::

            {
                "X": list,
                "y": list
            }
        """
        return self.subdataset.get_train_data(subset=self.subdataset_set)

    def get_test_data(self):
        """
        Get the test data from the run related subdataset set

        Returns
        -------
        dict
            Containing records and its labels::

            {
                "X": list,
                "y": list
            }
        """
        return self.subdataset.get_test_data(subset=self.subdataset_set)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status
        if status == "finished":
            self.finish_date = datetime.now()
    
    @property
    def results(self):
        """
        Get results

        Returns
        -------
        optapp.Result
        """
        return self._results

    @results.setter
    def results(self, result):
        self.status = "finished"
        self._results = result

    def get_info(self):
        """
        Get the summary of a run instance

        Returns
        -------
        dict
            Dict containing a run summary::

            {
                "id": <unique identifier>,
                "approach_id": <approach id>,
                "subdataset": <subdataset id>,
                "run_parameters": <hyperparameters of the run>,
                "status": <run status>,
                "results": <dict summarizing optapp.Result instance>,
                "creation_date": <run creationd date>,
                "submitted_date": <when run starts>,
                "finish_date": <when run finishes>,
                "subdataset_set": <subdataset set>
            }
        """
        return {
            "id": self.id,
            "approach_id": self.approach_id,
            "subdataset": self.subdataset.id,
            "run_parameters": self.run_parameters,
            "status": self.status,
            "results": self._results.get_info() if self.results else None,
            "creation_date": str(self.creation_date),
            "submitted_date": str(self.sumbission_date),
            "finish_date": str(self.finish_date),
            "subdataset_set": self.subdataset_set
        }

    def save(self):
        Run.collection(self.approach_id).save(self)

    def update(self):
        Run.collection(self.approach_id).update(self)

    @classmethod
    def load(cls, approach_id, id_):
        return cls.collection(approach_id).get(id_)

    def done(self):
        """
        Is the comuptation done?
        
        Returns
        -------
        boolean
        """
        return self.status == "finished"
