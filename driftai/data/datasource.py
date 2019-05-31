import os
import re
import inspect
import hashlib
from pathlib import Path
from abc import ABC, abstractmethod, abstractproperty

import pandas as pd
import numpy as np
from PIL import Image

from driftai.exceptions import DriftAIFileDatasourceNotCompatibeException, DriftAIMethodNotImplementedYetException
from driftai.utils import filepath_to_uri, uri_to_filepath, check_uri, get_file_extension, compile_path_pattern, import_from

class Datasource(ABC):
    """
    Abstract datasource
    """
    def __init__(self, data_uri):
        self.datasource = data_uri
        self.data = None

    @abstractmethod
    def get_infolist(self):
        """
        Get list of labeled indices

        Returns
        -------
        list of tuples
            First element of the tuple is the index and the second element is the label
        """
        pass

    @abstractmethod
    def get_data(self):
        """
        Get all datasource data
        """
        pass

    @abstractmethod
    def __getitem__(self, indices):
        """
        Get data by infolist

        Parameters
        ----------
        indices: list of items of infolist
            List of data indices 

        Returns
        -------
        dict
            Dict with X and y keys, contining the data and the labels
        """
        pass

    def get_uri(self):
        """
        Get datasource location URI formated

        Returns
        -------
        str
            Datasource location
        """
        return self.datasource

    def get_path(self):
        """
        Get the location of datasource

        Returns
        -------
        str
            File system datasource location
        """
        return str(Path(uri_to_filepath(self.datasource)).resolve())

    @abstractmethod
    def __len__(self):
        pass

    @staticmethod
    def load_from_data(data):
        """
        Create datasource from serialized data

        Parameters
        ----------
        data: dict
            Dictionary containing serialized datasource data

        Returns
        -------
        Datasource
        """

        datasource_class_ = import_from(data["module"], 
                                        data["class_name"])
        del data["class_name"]
        del data["module"]
        
        return datasource_class_(**data)

    def get_info(self):
        """
        Datasource summary

        Returns
        -------
        dict
            Dictionary used to serialize DriftAI Datasource instance
        """
        return {
            "module": self.__module__,
            "class_name": self.__class__.__name__,
            "path": self.get_uri()
        }


class FileDatasource(Datasource):
    """
    Datasource subclass
    Responsible of handling datasets comming from a local file like csv files
    """
    def __init__(self, path, label=None, first_line_heading=True):
        """
        Parameters
        ----------
        path_to_data: str
            Location of the dataset. Accept formats are:
                - Filesystem path
                - File URI
        label: str, optional
            Name of the label. If label is left to None the default label is assumed to be the last column
        first_line_heading: bool, optional
            If True considers that first line is the header

        """
        # check if uri
        # if not uri, convert it
        if not check_uri(path):
            path = filepath_to_uri(path)
        super().__init__(path)
        self._label = label
        self.first_line_heading = first_line_heading

    def __len__(self):
        if not self.data:
            self.data = self.get_data()
        return len(self.data)

    @property
    def label(self):
        if self._label:
            return self._label
        else:
            df = self.get_data()
            self._label = df.columns[-1]
            # If column hasn't got a name, 
            # cast the index (originaly numpy.int64) to python's int
            if not isinstance(self._label, str):
                self._label = int(self._label)
            return self._label

    def get_infolist(self):
        """
        Get list of labeled indices

        Returns
        -------
        list of tuples
            First element of the tuple is the index and the second element is the label

        Raises
        ------
        DriftAIFileDatasourceNotCompatibeException
            If file extension is not compatible with DriftAI
        """
        compatible_extensions = ["csv"]
        file_ext = get_file_extension(self.datasource)
        if file_ext == None:
            raise DriftAIFileDatasourceNotCompatibeException(self.datasource)

        if file_ext in compatible_extensions:
            self.data = self._load_csv()
        else:
            raise DriftAIFileDatasourceNotCompatibeException(file_ext)
        return self.data

    def _load_csv(self, has_label=True):
        """
        Loads a csv file, reading from datasource. Considers that first line is the header and if has_label, last
        variable is the label

        Parameters
        ----------
        has_labels: bool
            Indicates that the dataset has a label column (its always the last one)

        Returns
        -------
        tuple
            A tuple with: (index, the whole line content, data_type, label)
        """
        df = self.get_data()
        indices = list(range(df.shape[0]))
        labels = df[self.label].values.tolist()

        return list(map(list, zip(indices, labels)))


    def get_data(self):
        """
        Get the content of csv file

        Returns
        -------
        pandas.DataFrame
            DataFrame wrapping the csv content
        """
        params = dict()
        if not self.first_line_heading:
            params["header"] = None
        return pd.read_csv(self.get_path(), **params)
    
    def __getitem__(self, indices):
        """
        Get data by indices

        Parameters
        ----------
        indices: list of items in infolist

        Returns
        -------
        pd.DataFrame
        """
        # TODO: Lazy loading dataset (No load all file in memory)
        df = self.get_data().iloc[[i[0] for i in indices]]
        X = df.drop(self.label, axis=1).values
        y = df[self.label].values
        return dict(X=X, y=y)

    def get_info(self):
        return {
            **super(FileDatasource, self).get_info(),
            "first_line_heading": self.first_line_heading,
            "label": self.label
        }


class DirectoryDatasource(Datasource):
    def __init__(self, path, parsing_pattern):
        """
        Parameters
        ----------
        path: str
            Location of the dataset. Accept formats are:
                - Filesystem path
                - File URI
        parsing_pattern: Pattern to get the label and data from file. Example: {testset}/{class}/{filename}.[txt|tsv]

        """
        # check if uri
        # if not uri, convert it
        if not check_uri(path):
            path = filepath_to_uri(path)

        super(DirectoryDatasource, self).__init__(path)
        self.parsing_pattern = parsing_pattern.replace('/', os.path.sep)
        self._compiled_pattern = compile_path_pattern(self.parsing_pattern, 
                                                      self.get_path(),
                                                      'file_idx')

    def _parse_file(self, path_pattern, file_path):
        # Get attributes from parsing pattern
        t = re.match(path_pattern, file_path)
        if t:
            return {
                "file": file_path,
                "extension" : file_path.split(".")[1],
                **t.groupdict()
            }

    def get_infolist(self):
        """
        Get list of labeled indices

        Returns
        -------
        list of tuples
            First element of the tuple is the index and the second element is the label
        """
        info_list = []
        for root, _, files in os.walk(self.get_path()):
            for file in files:
                f = Path(root, file)
                p = self._parse_file(self._compiled_pattern, str(f.resolve()))
                if p:
                    info_list.append((p["file_idx"], p["class"]))

        return info_list


    def get_info(self):
        """
        Directory datasource summary

        Returns
        -------
        dict
            Dictionary used to serialize an DriftAI DirectoryDatasource instance
        """
        return {
            **super(DirectoryDatasource, self).get_info(),
            "parsing_pattern": self.parsing_pattern,
        }

    def get_data(self):
        """
        Get all data under the datasource path

        Returns
        -------
        list of tuples
            First element of the tuple is the index and the second element is the label
        """
        datalist = []
        for inf in self.get_infolist():
            blob = self.loader(str(Path(self.get_path(), inf[0])))
            y = inf[1]
            datalist.append(dict(X=blob, y=y))
        return datalist

    def __getitem__(self, info_list):
        data = dict(X=[], y=[])
        for idx, label in info_list:
            data["X"].append(self.loader(str(Path(self.get_path(), idx))))
            data["y"].append(label)
        return data

    @abstractproperty
    def loader(self, idx):
        pass

    def __len__(self):
        return len(self.data)


class ImageDatasource(DirectoryDatasource):

    def __init__(self, path, parsing_pattern="{testset}/{class}_{}.[png|jpg|jpeg]"):
        super(ImageDatasource, self).__init__(path=path, 
                                              parsing_pattern=parsing_pattern)

    def loader(self, idx):
        return np.asarray(Image.open(idx)).reshape(-1)
