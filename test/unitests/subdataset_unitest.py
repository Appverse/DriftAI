import unittest
import shutil
import re
from pathlib import Path

from optapp import set_project_path
from optapp.data import Dataset, SubDataset
from optapp.project import Project
from optapp.run import Run, RunGenerator
from optapp.db import DatabaseInjector

from test import testenv

class SubDatasetTest(unittest.TestCase):
    def setUp(self):
        """
        Sets a defalut path to dataset
        """
        set_project_path(testenv.MOCK_PROJECT_PATH)
        self.path_to_dataset = testenv.MOCK_DATASET
        self.path_to_test_dir = testenv.TEST_PATH
        self.aux_project_name = testenv.MOCK_PROJECT_NAME
        self.path_to_auxproj = testenv.MOCK_PROJECT_PATH
        self.project_default_name = testenv.DEFAULT_PROJECT_NAME

    def tearDown(self):
        testenv.delete_mock_projects()

    def test_generate_subdataset(self, method="train_test", by=0.8):
        """
        Creates a Project and a Dataset and links each other. Then creates a SubDataset out of the created Dataset.
        The subdataset are created using method and by paramenters
        
        Asserts
        -------
            - Indicies are not None
        """
        Project(path=self.path_to_test_dir, name=self.aux_project_name)
        ds = Dataset.read_file(path=self.path_to_dataset)
        ds.save()

        sbds = SubDataset(dataset=ds, method=method, by=by)
        self.assertIsNotNone(sbds.indices)

        return sbds

    def test_generate_subdataset_with_train_test_method(self):
        method = "train_test"
        by = 0.8

        sbds = self.test_generate_subdataset(method=method, by=by)
        sbds.save()

        return sbds

    def test_generate_subdataset_with_train_kfold_method(self):
        method = "k_fold"
        by = 5

        sbds = self.test_generate_subdataset(method=method, by=by)
        sbds.save()

        self.assertEqual(sbds.indices["method"], method)
        self.assertTrue(len(sbds.indices["sets"].keys()) == by)

        return sbds

    def test_load_subdataset_with_train_test_method(self):
        sbds1 = self.test_generate_subdataset_with_train_test_method()
        sbds2 = SubDataset.load(sbds1.id)
        self.assertTrue(sbds1 == sbds2)

        return sbds2

    def test_load_subdataset_with_kfold_method(self):
        sbds1 = self.test_generate_subdataset_with_train_kfold_method()
        sbds2 = SubDataset.load(sbds1.id)

        self.assertTrue(sbds1 == sbds2)

        return sbds2

    def test_load_subdataset_test_data_with_kfold_method(self):
        sbds = self.test_load_subdataset_with_kfold_method()

        for set_ in sbds.indices["sets"].keys():
            sbds.get_train_data(set_)


if __name__ == '__main__':
    unittest.main()
