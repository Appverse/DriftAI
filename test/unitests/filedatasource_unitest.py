import unittest
import re
from pathlib import Path

from optapp.data.datasource import FileDatasource
from test import testenv

class FileDatasourceTest(unittest.TestCase):
    def setUp(self):
        """
        Sets a defalut path to dataset
        """
        self.path_to_dataset = testenv.MOCK_DATASET

    def test_create_filedatasource(self):
        """
        Creates a FileDatasource instance
        
        Asserts
        -------
            - FileDatasource instance is not None
        
        Returns
        -------
        FileDatasource object instance
        """
        fds = FileDatasource(path=self.path_to_dataset)
        self.assertIsNotNone(fds)
        return fds

    def test_get_filedatasource_uri(self):
        """
        Creates a FileDatasource instance and check that the uri is in the correct form
        """
        fds = self.test_create_filedatasource()
        uri = fds.get_uri()
        self.assertRegex(uri, "^file:.*")


    def test_get_filedatasource_file_path(self):
        """
        Creates a FileDatasource instance and check that the FileDatasource.get_path() 
        method returns an existing file
        """
        fds = self.test_create_filedatasource()
        datafile_path = fds.get_path()

        self.assertTrue(Path(datafile_path).is_file())

    def test_get_filedatasource_infolist(self):
        """
        Creates a FileDatasource and applies method FileDatasource.get_infolist() to check it is a list of 4 element tuples
        
        Returns
        -------
        List of 4-elements tuple
        """
        fds = self.test_create_filedatasource()

        infolist = fds.get_infolist()
        for element in infolist:
            self.assertTrue(len(element) == 2)

        return infolist

if __name__ == '__main__':
    unittest.main()
