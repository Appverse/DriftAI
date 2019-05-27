import unittest
import shutil
import re
from pathlib import Path

from test import testenv
from optapp.run import ParameterGrid, RunGenerator
from optapp import Approach, Project, set_project_path
from optapp.data import Dataset, SubDataset
from optapp.utils import import_from

class RunGeneratorTest(unittest.TestCase):
    def tearDown(self):
        testenv.delete_mock_projects()
    
    def setUp(self):
        set_project_path(testenv.MOCK_PROJECT_PATH)

        self.p = Project(path=testenv.TEST_PATH, name=testenv.MOCK_PROJECT_NAME)
        
        self.ds = Dataset.read_file(path=testenv.MOCK_DATASET, 
                                    first_line_heading=False)
        self.ds.save()

        self.sbds = SubDataset(self.ds, method="k_fold", by=5)
        self.sbds.save()

        self.approach = Approach(self.p, "logistic_regression", self.sbds, path=str(Path(testenv.TEST_PATH, "lr")))
        shutil.copyfile(testenv.APPROACH_EXAMPLE, str(self.approach.script_path))
        self.approach.save()

    def test_generate_runs_from_subdataset(self):
        # Trick to load runnable approach
        LogisticRegressionApproach = import_from("test.lr.logistic_regression", "LogisticRegressionApproach")
        ra = LogisticRegressionApproach()
        
        # Generate the runs
        run_gens = RunGenerator.from_runnable_approach(ra)
        
        # Write runs to database
        ra.approach.runs = run_gens
        ra.approach.update()

        # Reload approach to test if runs were correctly stored
        approach = Approach.load(ra.approach.id)
        self.assertEqual(len(approach.runs), len(run_gens))

if __name__ == '__main__':
    unittest.main()
