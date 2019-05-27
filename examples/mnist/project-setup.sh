python download_mnist.py

opt new mnist-project

cd mnist-project

opt add dataset -p ../data/MNIST
opt generate subdataset MNIST --by 5 --method k_fold
opt generate approach random_forest --subdataset MNIST_k_fold_5

cp ../random_forest.py approaches/random_forest.py 

opt run random_forest