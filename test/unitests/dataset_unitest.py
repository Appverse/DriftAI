import unittest
import shutil
import re
from pathlib import Path

from optapp import set_project_path
from optapp.data import Dataset, FileDatasource
from optapp.project import Project
from optapp.db import DatabaseInjector

from tinydb import where
from test import testenv

class DatasetTest(unittest.TestCase):
    def setUp(self):
        set_project_path(testenv.MOCK_PROJECT_PATH)

        self.path_to_dataset = testenv.MOCK_DATASET
        self.path_to_test_dir = testenv.TEST_PATH
        self.aux_project_name = testenv.MOCK_PROJECT_NAME
        self.path_to_auxproj = testenv.MOCK_PROJECT_PATH
        self.project_default_name = "untitled_optapp_project"

    def tearDown(self):
        testenv.delete_mock_projects()

    def test_create_dataset(self):
        """
        Takes a dataset file and constructs a new dataset
        Asserts
        -------
            - If the object created is an instance of a Dataset object
            - If the datasource attribute is an instance of a FileDataset object
        
        Returns
        -------
        A Dataset object instance created from the dataset file
        """
        Project(name=self.aux_project_name, path=self.path_to_test_dir)
        ds = Dataset.read_file(path=self.path_to_dataset)
        self.assertIsInstance(ds, Dataset)
        self.assertIsInstance(ds.datasource, FileDatasource)
        return ds

    def test_dataset_get_info(self):
        """
        Creates a dataset from self.path_to_dataset and checks Dataset.get_info() method output.

        Asserts
        -------
            - Dataset's datasource is equal to Dataset.get_info datasource
            - Dataset's infolist is equal to infolist
            - Dataset's path is equal to path
            - Dataset's id is equal to id

        """
        ds = self.test_create_dataset()
        ds_info = ds.get_info()

        self.assertEqual(ds_info["datasource"]["path"], ds.datasource.get_uri())
        self.assertEqual(ds_info["infolist"], ds.infolist)
        self.assertEqual(ds_info["id"], ds.id)

    def test_save_dataset(self):
        """
        Creates a new Dataset instance and a new Project instance, 
        sets Datset instance to project's path and then saves
        the Dataset

        Asserts
        -------
            - The dataset is created in the expected collection

        Returns
        -------
        A Dataset instace, persisted to the filesystem
        """       
        ds = self.test_create_dataset()
        ds.save()

        self.assertIsNotNone(Dataset.load(ds.id))
        return ds

    def test_load_dataset(self):
        """
        Creates a Dataset intance persisted to the filesystem and loads it as a new Dataset instance
        
        Asserts
        -------
            - Equal method on datasets return True
        
        Returns
        -------
        Loaded Dataset instance
        """
        ds1 = self.test_save_dataset()
        ds2 = Dataset.load(ds1.id)

        self.assertEqual(ds1, ds2)
        return ds2

    def test_get_infolist(self):
        """
        Generate a new Dataset and check that infolist is created.
        
        Asserts
        -------
            - Dataset instace infolist is not None
            - Dataset.get_infolist() does not return None
        
        Returns
        -------
        List of 4-elements tuple
        """
        ds = self.test_create_dataset()
        self.assertIsNotNone(ds.infolist)

        ds_infolist = ds.infolist
        self.assertIsNotNone(ds_infolist)
        self.assertEqual(ds_infolist, ds.infolist)

        return ds_infolist

    def test_automatically_detect_clf(self):
        Project(name=self.aux_project_name, path=self.path_to_test_dir)
        ds = Dataset.read_file("test/resources/Iris.csv")
        self.assertEqual(ds.problem_type, "clf")

    def test_automatically_detect_binary_clf(self):
        Project(name=self.aux_project_name, path=self.path_to_test_dir)
        ds = Dataset.read_file("test/resources/titanic.csv", label="Survived")
        self.assertEqual(ds.problem_type, "binary_clf")

    def test_automatically_detect_regression(self):
        Project(name=self.aux_project_name, path=self.path_to_test_dir)
        ds = Dataset.read_file("test/resources/housing.csv", label="median_house_value")
        self.assertEqual(ds.problem_type, "regression")

    def test_directory_dataset(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
