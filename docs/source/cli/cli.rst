Optapp CLI
==========

The Command Line Interface to improve Optapp use experience

opt new
-------

The Optapp CLI makes easy to create the project structure.

Usage:

.. code-block:: console

    $ opt new <project-name>

Example:

.. code-block:: console

    $ opt new iris-project

opt add
-------

Add a new element to the project

Usage:

.. code-block:: console

    $ opt add --help
    Usage: opt add [OPTIONS] [dataset]

    Options:
    -p, --path TEXT           Path of dataset's datasource
    --heading / --no-heading  If the first line of CSV is the header or not
    -l, --label TEXT          The column name of the label. By default, the
                                label is the last column
    --parsing-pattern TEXT    Pattern to read the files inside the directory
    -d, --datatype [img]      Data type of files inside the directory

Dataset
~~~~~~~

Adds a new dataset to project.

Usage:

.. code-block:: console

    $ opt add dataset --path <dataset_path>

Examples:

Adding a csv file as Dataset:

.. code-block:: console

    $ opt add dataset --path path/to/dataset/Iris.csv
    Dataset with id Iris created

Adding a directory as Dataset:

.. code-block:: console

    $ opt add dataset --path path/to/dataset/MNIST/ --parsing-pattern {class}/{}.[png|jpg] --datatype img
    Dataset with id Iris created


opt generate
------------

Generates a new element based on the existent ones. For example: Crates a `Subdataset` from an existing `Dataset`.

Usage:

.. code-block:: console

    $ opt generate --help
    Usage: opt generate [OPTIONS] [subdataset|approach] IDENTIFIER

    Options:
    -s, --subdataset TEXT           In case item=approach. ID of the subdataset
                                    where approach will retrieve the data
    -m, --method [k_fold|train_test]
    --by TEXT                       In case method=k_fold, by is the number of
                                    folds. If method=train_test, by is the
                                    percentage of training instance
    -d, --dataset TEXT              ID of the dataset which new subdataset will
                                    be generated from
    --help                          Show this message and exit.

Subdataset
~~~~~~~~~~

Generates a dataset's partitions using K-folds or train test split.

Usage:

.. code-block:: console

    $ opt generate subdataset <dataset_id> --method <k_fold|train_test> --by <number of folds|train %>

Example:

.. code-block:: console

    # Creates a partition of a dataset where 25% of the instances belongs to the test set
    $ opt generate subdataset Iris --method train_test --by 0.75
    Subdataset with id Iris_train_test_0.75 created

    # Creates a partition of a dataset with 5 folds
    $ opt generate subdataset Iris --method k_fold --by 5
    Subdataset with id Iris_k_fold_5 created

Approach
~~~~~~~~

Creates a new file containing the `RunnableApproach` class with the specified name (Name should be written in camel_case). 

Usage:

.. code-block:: console

    $ opt generate approach <approach_name> --subdataset <subdataset containing the data to tune the approach model>

Example:

.. code-block:: console

    $ opt generate approach random_forest --subdataset Iris_k_fold_5

opt status
----------

Check the status of a running approach.

Usage:

.. code-block:: console

    $ opt status <approach_name>

Example:

.. code-block:: console

    $ opt status random_forest
    Loading approach data...
    Approach random_forest is still running
    [===>-------------------------------------] 7 % Done runs: 118 Total runs: 1520

opt run
-------

Run approach with the specified id.

Usage:

.. code-block:: console

    $ opt run <approach_name>

opt evaluate
------------

Evaluate approach's results and generates a csv file named `<approach_name>_evaluation.csv` where each line corresponds to a Run, and contains the ground truth and predicted labels, the metrics and the set of parameters used in each .

Usage:

.. code-block:: console

    $ opt evaluate <approach_name> -m <metric_1> -m <metric_2> ....