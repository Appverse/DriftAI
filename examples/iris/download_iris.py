import requests
from pathlib import Path

data_path = Path("./data")
data_path.mkdir(exist_ok=True)

data_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

r = requests.get(data_url)

if r.status_code == 200:
    print("Download ok...")
    with open(data_path.joinpath("iris.csv"), "wb") as f:
        f.write(r.content)
else:
    print("Failed downloading... (Status code: {})".format(r.status_code))
