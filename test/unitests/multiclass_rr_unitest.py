import unittest
import shutil
import re
from pathlib import Path

from optapp.data import Dataset, SubDataset
from optapp.run import Run, RunGenerator
from optapp.result_report import ResultReport, multiclass_recall, multiclass_precision, multiclass_f1
from optapp import Approach, Project, set_project_path
from optapp.utils import import_from

from test import testenv

class MulticlassResultReportTest(unittest.TestCase):
    def setUp(self):
        set_project_path(testenv.MOCK_PROJECT_PATH)

        self.path_to_dataset = testenv.IRIS_DATASET
        self.path_to_test_dir = testenv.TEST_PATH
        self.aux_project_name = testenv.MOCK_PROJECT_NAME
        self.path_to_auxproj = testenv.MOCK_PROJECT_PATH
        self.project_default_name = testenv.DEFAULT_PROJECT_NAME

        # Generate a project
        self.p = Project(path=self.path_to_test_dir, name=self.aux_project_name)
        
        # Add a dataset
        self.ds = Dataset.read_file(path=self.path_to_dataset,)
        self.ds.save()

        # Generate subdataset
        self.sbds = SubDataset(self.ds, method="k_fold", by=5)
        self.sbds.save()

        # set apporach
        self.approach = Approach(self.p, "decision_tree", self.sbds, path=str(Path(testenv.TEST_PATH, "dt")))
        shutil.copyfile(testenv.IRIS_APPROACH, str(self.approach.script_path))
        self.approach.save()

        # generate runs
        import_from("test.dt.decision_tree", "DecisionTreeApproach")().run()

    def tearDown(self):
        testenv.delete_mock_projects()

    def test_create_result_report(self):
        metrics = [multiclass_recall, multiclass_precision, multiclass_f1]
        r = ResultReport(approach=Approach.load(self.approach.id),
                         metrics=metrics)
        df = r.as_dataframe()       
        for m in [f.__name__ for f in metrics]:
            self.assertTrue(m in df.columns)

if __name__ == '__main__':
    unittest.main()