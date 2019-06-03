import io
import sys
import unittest
from pathlib import Path

from driftai.data import ImageDatasource
import testenv

# class DirectoryDatasourceTest(unittest.TestCase):
#     def test_directory_dataset(self):
#         path_to_data = "examples/mnist/data"
#         dd = ImageDatasource(path_to_data)
#         self.assertTrue(True)

#     def test_directory_dataset_get_infolist(self):
#         capturedOutput = io.StringIO()                  # Create StringIO object
#         sys.stdout = capturedOutput                     #  and redirect stdout.

#         path_to_data = "examples/mnist/data"
#         dd = ImageDatasource(path_to_data)
                
#         self.assertIsNotNone(dd)

# if __name__ == '__main__':
#     unittest.main()