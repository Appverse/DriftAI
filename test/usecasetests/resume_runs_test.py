import sys
from pathlib import Path 
import shutil

from optapp.data import Dataset, SubDataset
from optapp.run import RunGenerator
from optapp.result_report import ResultReport, recall, precision
from optapp import Approach, Project

path_to_project = Path(r"..").absolute()
project_name = "optapp"
project_path = Path(path_to_project, project_name)

if not project_path.is_dir():
    exit(-1)

proj = Project.load(str(project_path))

#resume subdataset
sbds = proj.get_subdataset(how="latest")

# set apporach
example_approach_path = r"./test/resources/approach_example.py"
a = Approach(proj, "example_approach", sbds)

# run experiment
a.run(kind="single")

rr = ResultReport(results_path=str(Path(sbds.path, "results")),
                  metrics = [recall, precision])

print(rr.as_dataframe())