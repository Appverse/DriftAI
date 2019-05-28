#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Optimise approaches to solve machine learning problems.

TODO: Change random seed to be -1 by default, which (in all scripts) will pick a random one, as in eval_approach.
TODO: Put time_estimate out of the pipeline, in a different library (it already existed).
"""

from datetime import datetime
import hashlib
import os
from pathlib import Path

from driftai.exceptions import DriftAIProjectDirNotExistsException, DriftAIProjectFileNotExistsException, \
    DriftAIProjectElementNotExistsException, DriftAIProjectNameExistsException, DriftAIProjectLoadPathIsNotDirException, DriftAIProjectWrongInfoFileStructureException

from driftai.utils import check_folder_structure, str_to_date
from driftai.approach import Approach
from driftai.data import SubDataset
from driftai.db import Database, Collections, DatabaseInjector

__author__ = "Pablo A. Rosado and Francesc Guitart"
__copyright__ = "Copyright 2018, GFT IT Consulting"
__credits__ = ["Pablo A. Rosado", "Francesc Guitart"]
__license__ = "Firefox"
__version__ = "0.0.1"
__maintainer__ = "Francesc Guitart"
__email__ = "francesc.guitart@gft.com"
__status__ = "Developement"


class Project(object):
    dir_components = {
        "project_files": "dir",
        "approaches": "dir",
        "driftai.db": "file"
    }

    dir_exceptions = {
        "file": DriftAIProjectFileNotExistsException,
        "dir": DriftAIProjectDirNotExistsException,
        "default": DriftAIProjectElementNotExistsException
    }

    def __init__(self, name=None, path=None, creation_date=None):
        """
        Parameters
        ----------
        name: str
            Project name. Default: untitled_driftai_project
        path: str
            Project path
        creation_date: datetime
            Creation date. Should not be set manually

        Raises
        ------
        DriftAIProjectNameExistsException
            In case project name already exists
        """
        self.name = self._get_name(path) if not name else name
        self.path = Path("." if not path else path).absolute()
        if self.path.stem != name:
            self.path = str(self.path.joinpath(self.name))
        else:
            self.path = str(self.path)

        self.creation_date = datetime.now() if not creation_date else creation_date
        
        if creation_date is None and self.exists():
            raise DriftAIProjectNameExistsException(self.path)
        else:
            self._maybe_create_path()

    @property
    def id(self):
        return self.name

    def save(self):
        # Workaround when project is created
        # Project is created at <current_dir>/project_name while user is at <current_dir>
        # We must force the database to create the new database in <current_dir>/project_name/driftai.db
        db = Database(self.path)
        db.insert(self.get_info())
        db.close()


    @classmethod
    def load(cls):
        """
        Creates a project from a tinydb file

        Parameters
        ----------
        path: str
            Project location

        Raises
        ------
        DriftAIProjectWrongInfoFileStructureException
           In case project structure is not valid

        Returns
        -------
        Project
            Returns the loaded project 
        """
        def check_project_content_structure(params):
            if not isinstance(params, dict):
                return False
            dict_contents = { "path", "creation_date", "name" }
            return dict_contents.intersection(list(params.keys())) == dict_contents

        project_content = DatabaseInjector.db().all()[0]
        
        if not check_project_content_structure(project_content):
            raise DriftAIProjectWrongInfoFileStructureException
        return cls(**project_content)

    def exists(self):
        """
        Check if project exists

        Returns
        -------
        bool
            True if project already exists
        """
        return Path(self.path).is_dir()


    def _create_project_structure(self):
        # Creates project structure
        project_path = Path(self.path)
        project_path.mkdir()
        
        for element in self.dir_components.keys():
            path = project_path.joinpath(element)
            if self.dir_components[element] == "dir":
                path.mkdir()
            elif self.dir_components[element] == "file":
                path.touch()
            else:
                raise Exception("Error creating project structure")

    def _get_name(self, path):
        # Generates a default project name
        temp_name = "untitled_driftai_project"
        temp_path = Path(path, temp_name).absolute()
        if temp_path.is_dir():
            i = 1
            while temp_path.is_dir():
                temp_name = "untitled_driftai_project_{}".format(i)
                temp_path = Path(path, temp_name).absolute()
                i += 1
        return temp_name

    def _maybe_create_path(self):
        # When loading a project check directory tree structure else, when creating a new project
        # creates tree structure
        if self.exists():
            check_folder_structure(self.path,
                                    Project.dir_components,
                                    Project.dir_exceptions)
        else:
            self._create_project_structure()
            self.save()


    def get_info(self):
        """
        Get project info
        
        Returns
        -------
        dict
            Dictionary containing the project info::

            {
                "path": <project_location>,
                "creation_date": <project's creation date>,
                "name": <project name>
            }
        """
        return {
            "path": self.path,
            "creation_date": str(self.creation_date),
            "name": self.name
        }

    def get_subdatasets(self):
        """
        Get all subdatasets

        Returns
        -------
        list(Subdataset)
            All subdatasets related to current project
        """
        return [SubDataset.load_from_data(p) for p in Collections.subdatasets().all()]

    def get_last_subdataset(self):
        """
        Get last subdataset
        
        Returns
        -------
        driftai.data.SubDataset
        """
        subdatasets = self.get_subdatasets()
        return sorted(subdatasets, key=lambda s: s.creation_date)[-1]

    def is_running(self):
        # TODO: Check if any approach is running
        # last_subdataset = self.get_last_subdataset()
        # rp = RunPool(subdataset_path=last_subdataset)
        # return rp.has_next()
        pass