import unittest
import shutil
import re
from pathlib import Path

from driftai.data import Dataset, SubDataset
from driftai.run import Run, RunGenerator
from driftai.result_report import ResultReport, recall, precision, f1
from driftai import Approach, Project, set_project_path
from driftai.utils import import_from

from test import testenv

class ResultReportTest(unittest.TestCase):
    def setUp(self):
        set_project_path(testenv.MOCK_PROJECT_PATH)

        self.path_to_dataset = testenv.MOCK_DATASET
        self.path_to_test_dir = testenv.TEST_PATH
        self.aux_project_name = testenv.MOCK_PROJECT_NAME
        self.path_to_auxproj = testenv.MOCK_PROJECT_PATH
        self.project_default_name = testenv.DEFAULT_PROJECT_NAME

        # Generate a project
        self.p = Project(path=self.path_to_test_dir, name=self.aux_project_name)
        
        # Add a dataset
        self.ds = Dataset.read_file(path=self.path_to_dataset)
        self.ds.save()

        # Generate subdataset
        self.sbds = SubDataset(self.ds, method="k_fold", by=5)
        self.sbds.save()

        # set apporach
        self.approach = Approach(self.p, "logistic_regression", self.sbds, path=str(Path(testenv.TEST_PATH, "lr")))
        shutil.copyfile(testenv.APPROACH_EXAMPLE, str(self.approach.script_path))
        self.approach.save()

        # generate runs
        import_from("lr.logistic_regression", "LogisticRegressionApproach")().run()

    def tearDown(self):
        testenv.delete_mock_projects()

    def test_create_result_report(self):
        metrics = ["recall", "precision", "f1"]
        r = ResultReport(approach=Approach.load(self.approach.id),
                         metrics = [recall, precision, f1])
        df = r.as_dataframe()       
        self.assertTrue(all(m in df.columns for m in metrics))

    def test_using_sklearn_metrics(self):
        from sklearn.metrics import classification_report
        r = ResultReport(approach=Approach.load(self.approach.id),
                         metrics = [classification_report])
        df = r.as_dataframe()       
        self.assertIsNotNone(df.classification_report[0])
