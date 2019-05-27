from pathlib import Path
import requests
import gzip

import numpy as np
from PIL import Image

data_url = "http://yann.lecun.com/exdb/mnist/"
data_files = [
    "train-images-idx3-ubyte.gz",
    "train-labels-idx1-ubyte.gz",
    "t10k-images-idx3-ubyte.gz",
    "t10k-labels-idx1-ubyte.gz"
]

data_path = Path("data", "MNIST")

data_path.mkdir(exist_ok=True, parents=True)

def save_file(file_name, file_content):
    with open(file_name, "wb") as f:
        f.write(file_content)

def save_images(image_file, label_file, out_path, num_images):
    img_file = gzip.open(data_path.joinpath(image_file),'r')

    image_size = 28

    img_file.read(16)
    buf = img_file.read(image_size * image_size * num_images)
    data = np.frombuffer(buf, dtype=np.uint8).astype(np.float32)
    data = data.reshape(num_images, image_size, image_size, 1)

    label_file = gzip.open(data_path.joinpath(label_file),'r')
    label_file.read(8)
    buf = label_file.read(1 * data.shape[0])
    labels = np.frombuffer(buf, dtype=np.uint8).astype(np.int64)

    digit_counter = {k:0 for k in range(11)}

    for i in range(num_images):
        img = Image.fromarray(data[i].reshape(28,28), "I")
        img.save(out_path.joinpath("{}_{}.png".format(labels[i], digit_counter[labels[i]])))
        digit_counter[labels[i]] += 1

    return data, labels
    
for f in data_files:
    r = requests.get("{}{}".format(data_url,f))
    if r.status_code == 200:
        save_file(data_path.joinpath(f), r.content)
    
data_path.joinpath("train/").mkdir(exist_ok=True)
data, labels = save_images("train-images-idx3-ubyte.gz", "train-labels-idx1-ubyte.gz", 
                            data_path.joinpath("train/"), 60000)

data_path.joinpath("test/").mkdir(exist_ok=True)
data, labels = save_images("t10k-images-idx3-ubyte.gz", "t10k-labels-idx1-ubyte.gz", 
                            data_path.joinpath("test/"), 10000)