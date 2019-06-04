import sys
import shutil
from pathlib import Path

from test import testenv

from driftai.data.dataset import Dataset
from driftai.project import Project
from driftai.approach import Approach
from driftai import set_project_path

sys.path.append(testenv.ROOT_PROJECT_PATH)

ds = Dataset.from_dir(testenv.ROOT_PROJECT_PATH+r"/examples/mnst_digit_classification_old/data")

proj_path = testenv.TEST_PATH
proj_name = "a"

if Path("{}\{}".format(proj_path, proj_name)).exists():
    shutil.rmtree(str(Path("{}\{}".format(proj_path, proj_name)).absolute()))

p = Project(name="a", path=testenv.TEST_PATH)
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
sys.path.append(testenv.MY_TEST_PATH + r"/a")
from approaches.my_approach import MyApproachApproach

MyApproachApproach().run(loader=lambda x: np.asarray(Image.open(x)).reshape(-1))