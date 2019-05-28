python download_mnist.py

dai new mnist-project

cd mnist-project

dai add dataset -p ../data/MNIST
dai generate subdataset MNIST --by 5 --method k_fold
dai generate approach random_forest --subdataset MNIST_k_fold_5

cp ../random_forest.py approaches/random_forest.py 

dai run random_forest