# Gather the data
# wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
# mkdir data/CIFAR-10 -p
# tar xvzf cifar-10-python.tar.gz -C data/CIFAR-10/
# rm cifar-10-python.tar.gz
# python unpickle_cifar10.py

# Create optapp project
opt new cifar-10-project
cd cifar-10-project

# Generate custom datasource
mkdir datasources
touch datasources/__init__.py
cp ../image_tensor_ds.py datasources/image_tensor_ds.py

# Create a dataset using custom datasource
opt add dataset --path ../data/CIFAR-10 \
                --parsing-pattern {}_{class}.png \
                --datatype datasources.image_tensor_ds.ImageTensorDatasource

# Generate subdataset
opt generate subdataset CIFAR-10 -m train_test --by .8

# Generate the approach
opt generate approach cnn --subdataset CIFAR-10_train_test_0.8
cp ../cnn.py approaches/cnn.py