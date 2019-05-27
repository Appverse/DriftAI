import hashlib
import string
from datetime import datetime
import dateutil.parser
from pathlib import Path

import numpy as np
from sklearn.model_selection import train_test_split

from .datasource import Datasource, FileDatasource, ImageDatasource
from optapp.utils import uri_to_filepath, maybe_make_dir, str_to_date
from optapp.db import Persistent, Collections

from optapp.exceptions import OptAppInvalidStructureException, \
                              OptAppInstanceExistsException, \
                              OptAppMethodNotImplementedYetException, \
                              OptAppInvalidStructureException


class Dataset(Persistent):
    """
    Indexed dataset over a datasource
    """

    def __init__(self, datasource, infolist=None, problem_type=None, creation_date=None, id=None):
        """
        Parameters
        ----------
        datasource: Datasource
            Datasource of the dataset
        problem_type: str, optional
            Objective of the algorithm.
            If `problem type` is not set manually, optapp will infere it automatically
            Possible values are: binary_clf, clf or regression
        creation_date: datetime
            Creation date of the dataset. Should not be set manually
        id: str
            Unique identifier for Dataset
        """
        self.datasource = datasource
        self.infolist = infolist or self.datasource.get_infolist()
        self.problem_type = problem_type or self._get_problem_type()
        self.creation_date = str_to_date(creation_date) or datetime.now()
        self._id = id or self._get_id()
        if creation_date is None and Dataset.collection().exists(self.id):
            raise OptAppInstanceExistsException("Dataset")

    @property
    def id(self):
        return  self._id

    @staticmethod
    def collection():
        """
        Get table containing datasets

        Returns
        -------
        TinyDB instance
        """
        return Collections.datasets()

    def get_labels(self):
        """
        Get all the labels

        Returns
        -------
        list
            List with all labels
        """
        return [x[1] for x in self.infolist]

    def _get_problem_type(self):
        # TODO: Is it really necessary?
        seen = set()
        labels = [i[-1] for i in self.infolist if i[-1] not in seen and not seen.add(i[-1])]
        if len(labels) == 2:
            return "binary_clf"
        # TODO: Think a better solution
        elif all([type(l) == str for l in labels]) or len(set(labels)) < 10:
            return "clf"
        else:
            return "regression"

    @staticmethod
    def from_dir(path, path_pattern=None, datatype="img"):
        """
        Create a Dataset from dir

        Parameters
        ----------
        path: str
            DataSource location path
        path_pattern: str, optional
            Pattern to generate metadate. If path_pattern is left to None the default path_pattern is taken
        datatype: str, optional
            Directory datatype

        Returns
        -------
        DirectoryDatasource
        """
        datasource_classes = {
            "img": ImageDatasource
        }

        if datatype not in datasource_classes:
            raise OptAppMethodNotImplementedYetException(
                "DirectoryDatasource with datatype {} not implemented yet".format(datatype))        

        datasource_parameters = dict(path=path)
        if path_pattern:
            datasource_parameters["parsing_pattern"] = path_pattern

        params = {
            "datasource": datasource_classes[datatype](**datasource_parameters),
            "id": Path(path).stem,
        }
        return Dataset(**params)

    @staticmethod
    def read_file(path, label=None, first_line_heading=True):
        """
        Create a Dataset from a file

        Parameters
        ----------
        path: str
            DataSource location path
        label: str, optional
            Name of the label. If label is left to None the default label is assumed to be the last column
        first_line_heading: bool, optional
            If True considers that first line is the header
        """
        params = {
            "datasource": FileDatasource(path, label, first_line_heading),
            "infolist": None,
            "id": Path(path).stem,
        }
        return Dataset(**params)

    @classmethod
    def load_from_data(cls, data):
        """
        Creates a Dataset object from serialized JSON data coming from TinyDB

        Parameters
        ----------
        data: dict
            JSON data from TinyDB

        Raises
        ------
        OptAppInvalidStructureException
            In case file keys are incorrect

        Returns
        -------
        optapp.Dataset
            New Dataset instance
        """
        def check_dataset_info_structure(params):
            dict_contents = {"datasource", "creation_date", "id", "infolist", "problem_type"}
            return isinstance(params, dict) and \
                    dict_contents.intersection(list(params.keys())) == dict_contents 

        if check_dataset_info_structure(data):
            data["datasource"] = Datasource.load_from_data(data["datasource"])
            return cls(**data)
        else:
            raise OptAppInvalidStructureException()

    def get_info(self):
        """
        Get info to serialize a Dataset instance

        Returns
        -------
        dict
            Dictionariy containing a Dataset object summary::

            {
                "datasource": dict containing path, first_line_heading and label of the datasource,
                "infolist": <TODO>,
                "problem_type": <multiclass clf, regression, binary clf>,
                "creation_date": <creation date of the dataset>,
                "id": <unique identifier>
            }
        """
        info = {
            "datasource": {
                **self.datasource.get_info()
            },
            "infolist": self.infolist,
            "problem_type": self.problem_type,
            "creation_date": str(self.creation_date),
            "id": self.id,
        }
        return info

    def generate_subdataset(self, method, by):
        """
        Creates a subdataset of the current Dataset

        Parameters
        ----------
        method: str
            Evaluation sets split approach.
            Can be: ``train_test`` ``k_fold``

        by: float, int
            If train_test method is specified, by represents the traininig set size. For example: .85
            If k_fold method is specified, `by` is the number of folds
        """
        return SubDataset(dataset=self, method=method, by=by)

    def get_data(self):
        """
        Get datasource data
        """
        return self.datasource.get_data()

    def __getitem__(self, indices):
        return self.datasource[np.array(self.infolist)[indices]]

    def _get_id(self):
        h = hashlib.md5(str(self.creation_date).encode('utf-8')).hexdigest()
        return h


class SubDataset(Persistent):
    def __init__(self, dataset, method, by=None, indices=None, id=None, creation_date=None):
        """
        Parameters
        ----------
        dataset: Dataset
            Optapp dataset which the current subdataset inherits from
        method: str
            Evaluation sets split approach.
            Can be: train_test, k_fold
        by: float, int, optional
            If train_test method is specified, by represents the traininig set size. For example: .85
            If k_fold method is specified, `by` is the number of folds
        indices: dict
            Contains the number of sets and the indices of each set::

            {
                "method": str
                "indices:" {
                    "train": list of int
                    "test": list of int
                }
            }

            Should not be set by the developer
        id: str, optional
            Unique identifier
        creation_date: str, datetime, optional
            Creation date of the subdataset. Should not be set manually
        """
        self.dataset = dataset

        # if indices are not passed as parameter, is required to generate indices
        if indices is None and by is None:
            raise TypeError(
                "missing one of the two arguments: 'indices' or 'by'")

        self.indices = indices or self._generate_indices(method=method, by=by)
        self.method = method
        self.by = by
        self.creation_date = str_to_date(creation_date) or datetime.now()
        self._id = id or self._get_id()

        if creation_date is None and SubDataset.collection().exists(self.id):
            raise OptAppInstanceExistsException("SubDataset")


    @property
    def id(self):
        return self._id

    @staticmethod
    def collection():
        """
        Get table containing subdatasets

        Returns
        -------
        TinyDB instance
        """
        return Collections.subdatasets()

    @classmethod
    def load_from_data(cls, data):
        """
        Loads a subdataset from data coming from TinyDB

        Parameters
        ----------
        data: dict
            JSON data

        Raises
        ------
        OptAppSubDatasetInfoFileWrongStructureException
            If data has worng keys

        Returns
        -------
        optapp.SubDataset
            New SubDataset instance
        """
        def check_subdataset_info_structure(params):
            if not isinstance(params, dict):
                return False
            dict_contents = {"dataset", "creation_date", "method", "by", "indices", "id"}
            return dict_contents.intersection(list(params.keys())) == dict_contents

        if check_subdataset_info_structure(data):
            data["dataset"] = Dataset.load(data["dataset"])
            return cls(**data)
        else:
            raise OptAppInvalidStructureException()

    def _get_id(self):
        return self.dataset.id + "_" + self.method + "_" + str(self.by)

    def _generate_indices(self, method="train_test", by=None):
        # Generate the indices depending on the method
        infolist = self.dataset.infolist

        if method == "train_test":
            train, test = self._train_test_split(
                infolist=infolist, split=by, seed=None)
            sets = {"0": {"train": train, "test": test}}

        elif method == "k_fold":
            sets = {}
            train_test_folds = self._k_fold_cv_split(
                infolist=infolist, split=by, seed=None)
            for k in range(by):
                train = train_test_folds[k]["train"]
                test = train_test_folds[k]["test"]
                sets[string.ascii_uppercase[k]] = {"train": train,
                                                   "test": test}
        # elif method == "stratified_train_test":
        # elif method == "bootstrap":

        else:
            raise OptAppMethodNotImplementedYetException()

        return {"method": method, "sets": sets}

    def _train_test_split(self, infolist, split, seed=None):
        indices = list(range(len(infolist)))
        return train_test_split(indices, train_size=split, test_size=1-split)

    def _k_fold_cv_split(self, infolist, split, seed=None):
        from sklearn.model_selection import KFold
        
        kf = KFold(n_splits=split, shuffle=True)
        indices = list(range(len(infolist)))

        folds = []
        for train_indices, test_indices in kf.split(X=indices):
            folds.append({
                "train": train_indices.tolist(),
                "test": test_indices.tolist()
            })
        return folds

    def get_info(self):
        """
        Get info to serialize a SubDataset instance
        
        Returns
        -------
        dict
            Contains subdataset essential information::

            {
                "dataset": str, parent dataset path,
                "creation_date": str, Subdataset creation date,
                "id": str,
                "indices": dict, structure specified at the costructor parameters documentation,
                "path": str, subdataset path
            }

        """
        return {
            "dataset": self.dataset.id,
            "creation_date": str(self.creation_date),
            "id": self.id,
            "indices": self.indices,
            "by": self.by,
            "method": self.method
        }


    def _get_data(self, subset, train_test):
        index = self.indices["sets"][subset][train_test]
        return self.dataset[index]

    def get_train_data(self, subset):
        """
        Get the training data of a subset

        Parameters
        ----------
        subset: str
            subset identifier

        Returns
        -------
        dict
            Containing each training set instance with its label::

            {
                "X": list,
                "y": list
            }

        """
        return self._get_data(subset, "train")

    def get_test_data(self, subset):
        """
        Get the test data of a subset

        Parameters
        ----------
        subset: str
            subset identifier

        Returns
        -------
        dict
            Containing all instances which belog to test set with its label::
            
                { 
                    "X": list,
                    "y": list
                }

        """
        return self._get_data(subset, "test")
    
    def _get_labels(self, train_test, subset):
        index = self.indices["sets"][subset][train_test]
        labels = np.array(self.dataset.get_labels())
        return labels[index].tolist()

    def get_train_labels(self, subset):
        """
        Get the labels of training set of an specific subset

        Parameters
        ----------
        subset: str
            subset identifier

        Returns
        -------
        list
            Ground truths of subset's training data
        """
        return self._get_labels('train', subset)

    def get_test_labels(self, subset):
        """
        Get the labels of test set of an specific subset

        Parameters
        ----------
        subset: str
            subset identifier

        Returns
        -------
        list
            Ground truths of subset's test data
        """
        return self._get_labels('test', subset)
