import unittest
from pathlib import Path
import shutil

import testenv

from driftai import set_project_path
from driftai.data import SubDataset, Dataset
from driftai import Approach, Project
from driftai.run import RunGenerator, Run
from driftai.utils import import_from

class ApproachTest(unittest.TestCase):
    def setUp(self):
        set_project_path(testenv.MOCK_PROJECT_PATH)

        self.p = Project(path=testenv.TEST_PATH, name=testenv.MOCK_PROJECT_NAME)
        self.ds = Dataset.read_file(path=testenv.MOCK_DATASET,
                                    first_line_heading=False)

        self.ds.save()

        self.sbds = SubDataset(self.ds, method="k_fold", by=5)
        self.sbds.save()

        self.approach = Approach(self.p, "logistic_regression", self.sbds, path=str(Path(testenv.TEST_PATH, testenv.MOCK_PROJECT_NAME)))
        shutil.copyfile(testenv.APPROACH_EXAMPLE, str(self.approach.script_path))
        self.approach.save()

    def tearDown(self):
        testenv.delete_mock_projects()

    def test_get_subdataset_runs(self):
        runnable = import_from(testenv.MOCK_PROJECT_NAME + ".logistic_regression", "LogisticRegressionApproach")
        runs = RunGenerator.from_runnable_approach(runnable())
        for run in runs:
            run.save()

        runs = Approach.load(self.approach.id).runs
        self.assertTrue(len(runs) > 0)
        for run in runs:
            self.assertIsInstance(run, Run)
        return runs

if __name__ == '__main__':
    unittest.main()
