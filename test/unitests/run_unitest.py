import unittest
import shutil
import re
from pathlib import Path

from optapp.run import Run, RunPool
from optapp.data import Dataset, SubDataset
from optapp import Approach, Project, set_project_path

from test import testenv

class RunTest(unittest.TestCase):
    def setUp(self):
        set_project_path(testenv.MOCK_PROJECT_PATH)

        self.path_to_dataset = testenv.MOCK_DATASET
        self.path_to_test_dir = testenv.TEST_PATH
        self.aux_project_name = testenv.MOCK_PROJECT_NAME
        self.path_to_auxproj = testenv.MOCK_PROJECT_PATH
        self.project_default_name = testenv.DEFAULT_PROJECT_NAME

        self.p = Project(path=self.path_to_test_dir, name=self.aux_project_name)
        self.ds = Dataset.read_file(path=self.path_to_dataset)
        self.ds.save()

        self.sbds = SubDataset(self.ds, method="k_fold", by=5)
        self.sbds.save()

        self.approach = Approach(self.p, "test_approach", self.sbds)
        shutil.copyfile(testenv.APPROACH_EXAMPLE, str(self.approach.script_path))
        self.approach.save()

    def tearDown(self):
        testenv.delete_mock_projects()

    def test_create_run(self):
        Run(
            approach_id = self.approach.id,
            subdataset = self.sbds,
            subdataset_set = "A",
            run_parameters = {"param1": 1, "param2": 2},
        )

    def test_create_run_and_save(self):
        run = Run(
            approach_id = self.approach.id,
            subdataset = self.sbds,
            subdataset_set = "A",
            run_parameters = {"param1": 1, "param2": 2},
        )
        run.save()
        data = Run.load(self.approach.id, run.id)
        self.assertIsNotNone(data)
        return run

    def test_load_run(self):
        run1 = self.test_create_run_and_save()
        run2 = Run.load(self.approach.id, run1.id)
        self.assertEqual(run1.id, run2.id)

    def test_create_runpool(self):
        # Force reload runs from database
        self.approach = Approach.load(self.approach.id)
        runpool = RunPool(self.approach.runs)

        for run in runpool.iteruns():
            self.assertTrue(isinstance(run, Run))

    def test_iterate_all_runs_runpool(self):
        self.approach = Approach.load(self.approach.id)
        runpool = RunPool(self.approach.runs)

        i = 0
        for run in runpool.iteruns():
            self.assertTrue(isinstance(run, Run))
            run.status = "finished"
            i += 1

        self.assertEqual(i, runpool.iter)

    def test_iterate_all_runs_runpool_twice(self):
        self.approach = Approach.load(self.approach.id)
        runpool = RunPool(self.approach.runs)

        i = 0
        for run in runpool.iteruns():
            self.assertTrue(isinstance(run, Run))
            run.status = "finished"
            i += 1
        self.assertEqual(i, runpool.iter)

        i = 0
        no_iterations = True
        for run in runpool.iteruns():
            no_iterations = False
        self.assertTrue(no_iterations)

if __name__ == '__main__':
    unittest.main()
