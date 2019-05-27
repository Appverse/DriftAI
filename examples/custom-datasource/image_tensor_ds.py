import numpy as np
from PIL import Image

import optapp as opt


class ImageTensorDatasource(opt.data.DirectoryDatasource):

    def loader(self, idx):
        return np.asarray(Image.open(idx)).reshape(32, 32, 3)
