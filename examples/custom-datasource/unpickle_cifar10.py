import pickle
from pathlib import Path

from PIL import Image
import numpy as np


def unpickle(file):
    with open(file, 'rb') as fo:
        data = pickle.load(fo, encoding='bytes')
    return data


def reshape_single_array(array):
    return np.transpose(np.reshape(array, (3, 32, 32)), (1, 2, 0))


data_path = Path("data", "CIFAR-10")
cifar_pickles_path = data_path.joinpath("cifar-10-batches-py")

meta_data_dict = unpickle(cifar_pickles_path.joinpath("batches.meta"))
cifar_label_names = meta_data_dict[b'label_names']
cifar_label_names = np.array(cifar_label_names)

# cifar_train_data_dict
    # 'batch_label': 'training batch 5 of 5'
    # 'data': ndarray
    # 'filenames': list
    # 'labels': list

counter = 0
for i in range(1, 3):
    cifar_train_data_dict = unpickle(cifar_pickles_path.joinpath("data_batch_{}".format(i)))
    labels_data = zip(cifar_train_data_dict[b'labels'], cifar_train_data_dict[b'data'])
    for label, array in labels_data:
        single_img_reshaped = reshape_single_array(array)
        img = Image.fromarray(single_img_reshaped.astype(np.uint8))
        img.save(str(data_path.joinpath('{}_{}.png'.format(counter, label))), "PNG")
        counter += 1
