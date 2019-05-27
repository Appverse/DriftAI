import sys
import shutil
from pathlib import Path

sys.path.append(r"C:\cygwin64\home\fcgr\code\optapp")

from optapp.data.dataset import Dataset
from optapp.project import Project
from optapp.approach import Approach
from optapp import set_project_path

ds = Dataset.from_dir(r"C:\cygwin64\home\fcgr\code\optapp\examples\mnst_digit_classification_old\data")

proj_path = r"C:\cygwin64\home\fcgr\code\optapp\test\my_tests"
proj_name = "a"

if Path("{}\{}".format(proj_path, proj_name)).exists():
    shutil.rmtree(str(Path("{}\{}".format(proj_path, proj_name)).absolute()))

p = Project(name="a", path=r"C:\cygwin64\home\fcgr\code\optapp\test\my_tests")
set_project_path(p.path)


info = ds.get_info()
ds.save()

sbs = ds.generate_subdataset(method="k_fold", by=5)
sbs.save()

from PIL import Image
import numpy as np

#tr_data = sbs.get_train_data("A", loader=lambda x: np.asarray(Image.open(x)).reshape(-1))
#ts_data = sbs.get_test_data("A", loader=lambda x: np.asarray(Image.open(x)))



a = Approach(project=p, name="my_approach", subdataset=sbs)
a.save()

shutil.copy2("my_approach.py", r"a/approaches/")

import sys
sys.path.append(r"C:\cygwin64\home\fcgr\code\optapp\test\my_tests\a")
from approaches.my_approach import MyApproachApproach

MyApproachApproach().run(loader=lambda x: np.asarray(Image.open(x)).reshape(-1))