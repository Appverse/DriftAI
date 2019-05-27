python download_iris.py

opt new iris-classifier-project

cd iris-classifier-project

opt add dataset -p ../data/iris.csv
opt generate subdataset iris --by 5 --method k_fold
opt generate approach logistic_regression --subdataset iris_k_fold_5

cp ../logistic_regression.py approaches/logistic_regression.py 

opt run logistic_regression