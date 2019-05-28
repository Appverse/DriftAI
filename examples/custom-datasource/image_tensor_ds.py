import numpy as np
from PIL import Image

import driftai as dai


class ImageTensorDatasource(dai.data.DirectoryDatasource):

    def loader(self, idx):
        return np.asarray(Image.open(idx)).reshape(32, 32, 3)
