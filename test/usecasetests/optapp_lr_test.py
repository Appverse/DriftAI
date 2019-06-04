import shutil
from pathlib import Path

from driftai.data import Dataset, SubDataset
from driftai.run import RunGenerator
from driftai.result_report import ResultReport, precision, recall
from driftai import Approach, Project
from test import testenv

def clean(project):
    shutil.rmtree(project.path)

# create new project
path_to_project = str(Path(".").absolute())
project_name = "test_project"
project_path = Path(path_to_project, project_name)

# If project exist delete and recreate it
if project_path.is_dir():
    proj = Project.load(project_path)
    clean(proj)

proj = Project(name="test_project", path=path_to_project)

# add a datasource
path_to_dataset = str(Path(testenv._RESOURCES_PATH, "test_dataset.csv"))
ds = Dataset.read_file(path_to_dataset)
# ds.set_project_path(proj.path)
ds.save()

# create subdataset
sbds = SubDataset(ds, method="k_fold", by=5)
sbds.save()

# set apporach
example_approach_path = str(Path(testenv._RESOURCES_PATH, "approach_example.py"))
param_path = r"./test/resources/parameters_example.yml"
a = Approach(proj, "approach_example", sbds)
shutil.copyfile(example_approach_path, str(a.script_path))
shutil.copyfile(param_path, str(a.params_path))
a.save()

# generate runs
rg = RunGenerator.from_approach(a)

# run experiment
a.run(kind="single")

rr = ResultReport(results_path=str(Path(a.path, "results")),
                  metrics = [recall, precision])

print(rr.as_dataframe())