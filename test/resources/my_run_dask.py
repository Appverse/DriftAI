import time
import sys

from driftai.data import SubDataset
from driftai.run import RunPool
from driftai.result_report import Result

import dask.bag as db
from dask.distributed import Client

import warnings
from dask.distributed import Client
from dask import delayed

subdataset_path = sys.argv[1]
n_workers = sys.argv[2]
job_window = sys.argv[3]
try:
    dask_endpoint = sys.argv[4]
    client = Client(dask_endpoint)
except IndexError:
    client = Client(processes=False)
    pass

def learn(train_data, parameters):
    from sklearn.linear_model import LogisticRegression
    lr = LogisticRegression(**parameters)
    time.sleep(3)
    lr.fit(**train_data)
    return lr

def inference(model, test_data):
    output = model.predict(test_data["X"])
    return output

def my_func(x):
    print(x[2])
    m = learn(train_data=x[0],parameters=x[2])
    o = inference(model=m, test_data=x[1])
    return o

sbs = SubDataset.load(path=subdataset_path)
runpool = RunPool(subdataset_path=sbs.path)

run_list = []
for run in runpool.iteruns():
    run.set_status("finished")
    run_list.append(run)

i=0
window=int(job_window)

while (i*window) < len(run_list):
    print([r.get_train_data()["X"].index for r in run_list[i*window:(i+1)*window]])
    run_data = [(r.get_train_data(), r.get_test_data(), r.get_parameters()) for r in
        run_list[i*window:(i+1)*window]
    ]
    job_bag = db.from_sequence(run_data, npartitions=int(n_workers))
    distr_run = job_bag.map(lambda x: my_func(x))
    results = distr_run.compute()
    for r in zip(run_list[i*window:(i+1)*window], results):
        r[0].resutlt = Result(0, r[1])
        r[0].save()
    i+=1