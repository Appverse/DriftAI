python download_iris.py

dai new iris-classifier-project

cd iris-classifier-project

dai add dataset -p ../data/iris.csv
dai generate subdataset iris --by 5 --method k_fold
dai generate approach logistic_regression --subdataset iris_k_fold_5

cp ../logistic_regression.py approaches/logistic_regression.py 

dai run logistic_regression