import unittest
from pathlib import Path 
import shutil
import re
import warnings

from driftai.data import Dataset, SubDataset
from driftai.run import RunGenerator
from driftai import Approach, Project, set_project_path
from driftai.utils import import_from
from driftai import set_project_path
# from driftai.exceptions import DriftAIProjectNameExistsException

import testenv


class ProjectTest(unittest.TestCase):
    def setUp(self):
        """
        Defines paths to the current test folder and the default project name self.project_name. If the folder already
        exists, it is deleted recursively
        """
        self.path_to_test_dir = testenv.TEST_PATH
        self.project_name = testenv.MOCK_PROJECT_NAME
        self.project_default_name = testenv.DEFAULT_PROJECT_NAME
        self.path_to_project = testenv.MOCK_PROJECT_PATH
        if Path(self.path_to_project).is_dir():
            shutil.rmtree(self.path_to_project)
        self.project = None

    def tearDown(self):
        testenv.delete_mock_projects()

    def test_create_new_project_with_name(self):
        """
        Creates a new Project given a path to the local file system and the project name
        
        Asserts
        -------
            - The project path is created
            - Exists property is true
        """
        set_project_path(testenv.MOCK_PROJECT_PATH)

        p = Project(name=self.project_name,
                    path=self.path_to_test_dir)

        self.assertEqual(p.path, self.path_to_project)
        self.assertTrue(p.exists())


    def test_create_new_project_without_name(self):
        """
        Creates a new Project given a path to the local file system without the project name
        
        Asserts
        -------
            - The project path is created
        """
        p = Project(path=self.path_to_test_dir)
        set_project_path(p.path)
        path_to_noname_project = Path(self.path_to_test_dir, self.project_default_name)
        self.assertEqual(p.path, str(path_to_noname_project))

    def test_create_two_projects_without_name(self):
        """
        Creates a new Project given a path to the local file system without the project name and then creates a new
        Project without name. The expected behaviour is that Projects generates a new name.
        
        Asserts
        -------
            - The first project path is created using the default name when no name is provided
            - The second project generates a new default name
        """

        p1 = Project(path=self.path_to_test_dir)
        p2 = Project(path=self.path_to_test_dir)
        set_project_path(p1.path)

        path_to_noname_project1 = Path(self.path_to_test_dir, self.project_default_name)
        path_to_noname_project2 = Path(self.path_to_test_dir, "{}_{}".format(self.project_default_name, 1))

        self.assertEqual(p1.path, str(path_to_noname_project1))
        self.assertEqual(p2.path, str(path_to_noname_project2))


    # def test_create_the_same_project_twice(self):
    #     """
    #     Creates a new Project given a path to the local file system without the project name and then creates a new
    #     Project with the same name. The expected behaviour is that the second project creation raises and Exception.
    #
    #     Asserts
    #     -------
    #         - The first project path is created using the default name when no name is provided
    #         - The second project generates an Exception
    #     """
    #     p1 = Project(path=self.path_to_test_dir)
    #     with self.assertRaises(DriftAIProjectNameExistsException):
    #         Project(path=self.path_to_test_dir, name=p1.name)
    #
    # def test_create_two_projects_with_same_name(self):
    #     """
    #     Creates a new Project given a path to the local file system and then creates a new
    #     Project with the same name. The expected behaviour is that the second project creation raises and Exception.
    #
    #     Asserts
    #     -------
    #         - The first project path is created
    #         - The second project generates an Exception
    #     """
    #     set_project_path(testenv.MOCK_PROJECT_PATH)
    #
    #     p1 = Project(path=self.path_to_test_dir, name=self.project_name)
    #     with self.assertRaises(DriftAIProjectNameExistsException):
    #         Project(path=self.path_to_test_dir, name=p1.name)

    def test_load_project(self):
        """
        Loads a project using a created project.
        
        Asserts
        -------
            - Both project paths are equal
        """
        self.test_create_new_project_with_name()
        p = Project.load()
        self.assertEqual(p.path, self.path_to_project)
        return p

    def test_load_project_from_non_project_dir(self):
        """
        Loads a project from a directory that is not a project
        
        Asserts
        -------
            - Raises the proper exception
        """
        set_project_path('no_exists')
        with self.assertRaises(FileNotFoundError):
            Project.load()

    def test_project_exists(self):
        """
        Loads a project using a created project and check that method exists returns True
        
        Asserts
        -------
            - Project.exists() returns True
        """
        self.test_create_new_project_with_name()
        p = Project.load()
        self.assertTrue(p.exists())

    def test_get_project_info(self):
        p = self.test_load_project()
        project_info = p.get_info()

        self.assertEqual(p.name, project_info["name"])
        self.assertEqual(p.path, project_info["path"])
        self.assertEqual(p.creation_date, project_info["creation_date"])

    def test_get_latest_subdataset(self):
        p = self.test_load_project()

        ds = Dataset.read_file(path=testenv.MOCK_DATASET, 
                               first_line_heading=False)
        ds.save()

        method = "k_fold"
        by = 5

        sbds1 = SubDataset(ds, method=method, by=by)
        sbds1.save()
        sbds2 = SubDataset(ds, method=method, by=by*2)
        sbds2.save()

        l_sbds = p.get_last_subdataset()

        self.assertEqual(l_sbds.id, sbds2.id)

if __name__ == '__main__':
    unittest.main()
