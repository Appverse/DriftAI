=======================================================
Using driftai to train a classifier on the MNIST dataset
=======================================================

In the Iris dataset example we have seen how to use driftai client to train a classifier over the Iris dataset. One of the benefits of driftai is that it has been designed to let the programmer to use its API to build its own scripts. This way, using the API, the programmer can automate the execution and extend driftai features programatically.


DriftAI has a series of benefits on how to organise and run Machine Learning worflows. This example shows how driftai can be used to train a classifier on the MNIST dataset.

This tutorial asumes that the programmer (you, for example) has already installed driftai in her machine. We also asume that the programmer has downladed driftai somewhere in its local drive and the path is in `$OPTAPP_HOME` in the environment variable and that you have a `OPTAPP_HOME` home in the script we are going to write.


Before we start trainig models we will download the MNIST dataset and store it as a valid driftai format.

Download the data
-----------------

To download the MNIST dataset, first copy the downloader to the current directory:

``cp %OPTAPP_HOME%/examples/download_mnist.py .``

Then run :

``python download_mnist.py``

This script will download data from the The MNIST Database (http://yann.lecun.com/exdb/mnist/index.html) and generate a tree source with the data. This tree source has to main folders (tain and test) and in each folder has a set of images. Each image has an idetifier with the following shape: <img_label>_<img_id>.png, where <img_label> is the label of the image  and <img_id> is an autonumeric index starting from 0 for each image label. As an example, we can find train/0_0.png which is the first 0 labelled image, and we can also find train/1_0.png or train/0_100.png.

Create the driftai script
------------------------

After having driftai installed and having downloaded MNIST data, all the needed material is a code editor.

Open a python script and import all the necessary dependencies

.. code-block:: python

    from driftai import set_project_path
    from driftai.project import Project
    from driftai.data.dataset import Dataset
    from driftai.approach import Approach

The imports show how driftai is internally organized and during the rest of the tutorial we will take a look on how can we use each of the driftai components to run our project.

Project Creation
^^^^^^^^^^^^^^^^

The first thing we want to do is to create our project scheme. We can also load an existing project, but in this tutorial we asume that the project needs to be created.

+-------------------------------------------------------------+
| Info                                                        |
+=============================================================+
| For more info on to how to Project works, refer to: TODO... |
+-------------------------------------------------------------+

.. code-block:: python

    proj_path = r"C:\path_to_my_project\"
    proj_name = "mnist_example"

    p = Project(name=proj_name, path=proj_path)

This automatically will create a new directory in "C:/path_to_my_project/my_project/", with the following contents:

::

    mnist_example
    ├── approaches
    ├── project_files
    └── driftai.db

Where:
    * approaches will contain the code for the apporaches we want to add to the project
    * project_files will contain metadata regardin the project
    * driftai.db will contain most of the information of the project execution, ranging from runs configuration to results

Dataset Creation
^^^^^^^^^^^^^^^^

Once we have a project defined, we have to create a `Dataset`. As we have downloaded the MNIST dataset as a set of images in several directories, we want to use the `Dataset` method `from_dir`.

.. code-block:: python

    ds = Dataset.from_dir("{}/mnist_data".format(OPTAPP_HOME),
                          datatype='img')

+------------------------------------------------------------------+
| Info                                                             |
+==================================================================+
| We can tackle different directory structures , refer to: TODO... |
+------------------------------------------------------------------+

Once we created the `Dataset`, as we are working outside the project directory, we have to change the path where driftai looks for the database:

.. code-block:: python
    # This will let us execute driftai scripts from any directory
    set_project_path(p.path) 
    ds.save()

After this, the dataset has been registered to our current project.

Subdataset Creation
^^^^^^^^^^^^^^^^^^^

A subdataset is a subset of a dataset. How this subset is generated, depends on the strategy we choose. DriftAI provides some implemented strategies, but it also provides enough fleixbility to extend and implement your own subdataset generation.

.. TODO: make a tutorial on how to extend subdataset generation

To generate a subdataset using k-fold Cross Validation, we just have to add the following lines:

.. code-block:: python

    sbs = ds.generate_subdataset(method="k_fold", by=5)
    sbs.save()

Where we use the method `generate_subdataset` passing the argument `k_fold` and the number of folds that we want (using `by` argument). Then we have to save the `Subdataset` we've just generated.

Approach Creation
^^^^^^^^^^^^^^^^^

Once we have a `Project` and a `Subdataset` we can create our `Approach`.

.. code-block:: python

    a = Approach(project=p, name="random_forest", subdataset=sbs)
    a.save()

This will modify our project structure:

::

    mnist_example
    ├── approaches
    │   └── random_forest.py
    ├── project_files
    └── driftai.db

We can see tha under `approaches`, we have a new Python script, named random_forest.py. If we take a look at the script we'll find that there's some code in it:


+--------------------------------------------------------------------------------------+
| Note                                                                                 |
+======================================================================================+
| Note that the following code will be outside the script we are creating for training |
+--------------------------------------------------------------------------------------+


.. code-block:: python

    from driftai import RunnableApproach
    from driftai.run import single_run

    @single_run
    class RandomForestApproach(RunnableApproach):

        @property
        def parameters(self):
            """
            Declare your parameters here
            """
            return None

        def learn(self, data, parameters):
            """
            Define, train and return your model here
            """
            return None

        def inference(self, model, data):
            """
            Use the injected model to make predictions with the data
            """
            return None

In the `learn` function we'll have to define the logic to train each fold/parameters combination. DriftAI will take control of how the arguments `data` and `parameters` are passed to the function. You have to return the trained model at the end of the function. For example, let's define the training part of a LogisticRegression:

.. code-block:: python

    from sklearn.ensemble import RandomForestClassifier

    def learn(self, data, parameters):
        """
        Define, train and return your model here
        """
        return RandomForestClassifier(**parameters).fit(**data)


In the `inference` function we'll use the trained the model to predict results over the test data. Again driftai will manage which data and will take care of providing the propper model. Depending on the model well have to change the predict function, but using the LogisitRegressor form scikit-learn, it will look like:

.. code-block:: python

    def inference(self, model, data):
        """
        Use the injected model to make predictions with the data
        """
        return model.predict(data["X"])

Finally, in `parameters` function we'll define the parameters space to define the ranges where we'll search the best parameters for our model. The parameters will have to be defined using the data types defined in `driftai.parameters`. For example, in our example we have defined:

.. code-block:: python

    from driftai.parameters import FloatParameter, BoolParameter

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

DriftAI will generate a search space using these parameter ranges. These parameters will be passed to inference.

Once we have defined the logics for training and predicting, and the parameter space definition in `my_approach.py` we're ready to continue with our otpapp run script.

For our convenience we may want to define `random_forest.py` out of the apporach directory, an the copy it into there. Like this:

.. code-block:: python

    import shutil
    shutil.copy2("random_forest.py", r"{}/{}/approaches/".format(proj_path, proj_name))

Finally, to run our `Approach` we'll have to define the following lines:

.. code-block:: python

    import sys
    sys.path.append("{}/{}".format(proj_path, proj_name))
    from approaches.random_forest import RandomForestApproach

    from PIL import Image
    import numpy as np

    RandomForestApproach().run()

First we add the path to our approaches into our `PYTHONPATH` so we can then load the approach as a package.

Once we have this, then we can run the approach.

Conclusion
----------

This tutorial covers two main driftai features. In one hand we have seen how to use driftai through its API, so you can define your own running scripts.

On the other hand we have seen how to define a datasource that handles data from a directory, this is very useful when dealing with Images like the MNIST dataset.