======================================================
Using driftai to train a classifier on the Iris dataset
======================================================

DriftAI has a series of benefits on how to organise and run Machine Learning worflows. This example shows how driftai can be used to train a classifier on the Iris dataset.

This tutorial asumes that the user (you, for example) has already installed driftai in her machine. `

Before we start trainig models we will download the Iris dataset and store it as a valid driftai format.

+----------------------------------------------------+
| Note                                               |
+====================================================+
| At the current moment only csv files are supported | 
+----------------------------------------------------+

---------------------------------
Setting up the project
---------------------------------

To create a new driftai project run:
.. code-block:: shell

    $ dai new <project_name>

Where ``<project_name>`` is the name you want to set to the current project. As we will train a classifier for the Iris dataset we will run ``dai new iris_classifier``.

After doing this we can check that a new directory has been created in our current path. It has some content, and the file tree is the following one:
::

    iris_classifier
    ├── approaches
    ├── project_files         
    └── driftai.db

This is the main project folder and each subfolder will contain the necessary onformation to store the workflow configuration files and logs. Let's walk through each of these files and directories:
    * approaches: this directory will contain one subdirectory for each apporach runned or to be runned. The main piece of information of an approach is the approach script that will contain the logic for training and inferring a model. Additionally we can define the parameters which the model will take during the training step.
    * project_files: TO BE DONE
    * driftai.db: This embedded database will contain the meta information about the project ant all the realated information about driftai objects like the datasets, subdatasets, runs, approaches, etc.

The next steps in the tutorial will show how to define a dataset from an external source (i.e. the Iris dataset) and how to generate a subdataset for a specific approach.

Download the data
---------------------------------

To download the Iris dataset first copy the downloader to the current directory:

``cp %OPTAPP_HOME%/examples/download_iris.py .`` 

Then run :

``python download_iris.py`` 

This script will download data from the UCI Machine Learning Repository and generate a csv file with the data. We won't go into details about dataset structure (we know it's not a good practice), but we want to show how transparent driftai is regarding the underlying data.

Create a dataset
-----------------

Let's import/generate a dataset from a csv file. As we said previously, we have already downloaded the Iris dataset somewhere in our local drive. Let's assume that the data is in ``C:/path_to_my_project/data/iris.csv``. We will load the data using the following command:

.. code-block:: shell

    $ dai add dataset -p C:/path_to_my_project/data/iris.csv

After doing this, the expected output is:

.. code-block:: shell
    
    Dataset with id iris created

The main change here is that driftai has added a new datasets into driftai.db(You can explore it as is a JSON formated file). This new dataset instance will contain: creation date, a description of the datasource including its path to the csv fle, an id, and the infolist, which are the parameters used to generate an driftai's Dataset object.

Probably infolist is the most important thing in this new file, as it will contain an index with a short description and a label for each instance of the dataset. This infolist will be the basis for creating new subdatasets in the future.

Generate a subdataset
---------------------

Before coding any model training procedure we will have to decide which strategy we will follow in the training step. For example, we may generate a subdataset splited in 5 folds to run a training procedure using 5-fold Cross Validation strategy. To do so, we have to run the following command:

.. code-block:: shell
    
    $ dai generate subdataset iris --by 5 --method k_fold

This will generate a new Subdataset entry on driftai.db with a certain id (it will be outputed when crating the dataset) that will contain the necessary metadata for feeding the logics within the runnable apporach script. The data will be feed transparently, no matter the strategy defined in subdataset, to the apporach script.

Define a runnable apporach
--------------------------

A runnable approach will have to main pieces:
    * A subdataset, that's why we have generated a subdataset before we create the apporach.
    * An apporach. We have to create an apporach using the following command: 

.. code-block:: shell
    
    $ dai generate approach logistic_regression --subdataset <subdataset_id>

Where ``logistic_regression`` is the name of the approach and 
``<subdataset_id>`` is the id of the subdataset we generated. An apporach will be contained in a directory with the following structure:
::

    iris_classifier
    ├── approaches
    │   └── logistic_regression.py
    └── driftai.db

We are only one step to go and run our approach, before that, let's explore what we've just created in the database.
    * A set of runs each containing on training/validation step
    * results where each result will contain the result of a run if it has been executed and finished correctly
    * logistic_regression.py will contain the code for the train and inference logics. Note that this script has been generated automatically and it is expected that the driftai user (this is you), fills the different methods within this skeleton.

Once we now a little bit more about each component in the approach directory, we can fill ``logistic_regression.py`` script. Let's see how it looks like:


.. code-block:: python

    from driftai.approach import RunnableApproach, Approach
    from driftai.run import single_run


   @single_run
   class LogisticRegressionApproach(RunnableApproach):

      @property
      def parameters(self):
          """
          Declare your parameters here
          """
          return []

      def learn(self, data, parameters):
          """
          Define, train and return your model here
          """
          return None #return the trained model

      def inference(self, model, data):
          """
          Use the injected model to make predictions with the data
          """
          return None #return predictions

DriftAI just needs three things:

* learn: a learning procedure to generate a model. Here we can use any technology we want. In the Iris dataset case we will use scikit-learn. We can, for example, use a linear regressor:

.. code-block:: python

    def learn(self, data, parameters):
        """
        Define, train and return your model here
        """
        lr_parameters = {
            "random_state" : 0, 
            "solver" : 'lbfgs', 
            "multi_class" : 'multinomial',
            **parameters
        }
        clf = LogisticRegression(**lr_parameters).fit(data["X"], data["y"])

        return clf 

+-----------------------------------------------------------------------------------------+
| Note                                                                                    |
+=========================================================================================+
| Note that we have defined some fixed parameters: Todo: tutorial on parameter definition |
+-----------------------------------------------------------------------------------------+

* inference: within this part we do the inference over a train or validation set (depending on the strategy we configured). Note that this is done transparently. This will generate the results.

.. code-block:: python

    def inference(self, model, data):
        """
        Use the injected model to make predictions with the data
        """
        return model.predict(data["X"])

* parameters: within this part, we will define a range of parameters to search for the best combination. Note that, the more parameters we define, the greatest is the time spent training and testing. Parameters are defined using the following syntax:

.. code-block:: python

    @property
    def parameters(self):
        """
        Declare your parameters here
        """
        pars = [
            FloatParameter("tol", 1e-4, 1, 10),
            FloatParameter("C", 1, 3, 10),
            BoolParameter("fit_intercept")
        ]

        return pars

In this case we have defined three parameters. Two of them (C and tol) are float parameters, and we defined a range and a step, so in C paramete case it will generate 10 values from 1 to 3.

Don't forget to import necessary packages:

.. code-block:: python

    from driftai.parameters import FloatParameter, BoolParameter
    from sklearn.linear_model import LogisticRegression

Create a runner
---------------

Once we have our approach, we can create the runner that will control the execution of our approach. The user will only have to create a ``runner.py`` file in the root direcotry of the project, using the next pattern:

.. code-block:: python

    from approaches.logistic_regression import LogisticRegressionApproach

    LogisticRegressionApproach().run()

Once we are done, we just have to run the following command:
``python runner.py``

We shoud see a progress bar showing the training process.

Get the results
----------------

To see the list of your current projects, run:

.. code-block:: shell

    $ dai results list

Once we have all our approaches, we can see the results of a certain approach, just running ``dai status <apporach_id>``, in our case:

.. code-block:: shell

    $ dai status logistic_regression

Conclusions
-----------

We showed how to use DriftAI to train a simple example with logistic regression and k-fold cross validation. This example can be extended to more compex approaches. See the following tutorials:

TO BE DONE