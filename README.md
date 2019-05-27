# Optapp

Optapp is a Machine Learning development framework. It's main aim is to standardize the model development cycle increasing the rapidness and a higher technology flexibility, allowing the inclusion of several libraries. It establishes a common framework among developers for model reproductivity and testing.

## Install

1. Clone the project

```
$ git clone https://git.gft.com/gft-ai-tools/optapp.git && cd optapp
```
2. You need python and pip installed. (If don't have it download it from https://www.python.org/)

3. You need Visual C++ Build Tools. Download it from https://www.microsoft.com/es-es/download/confirmation.aspx?id=48159

4. Install OptApp with ``setup`` script.

```
$ python setup.py install
```

## Using CLI to create and run a project

1. Create a project and navigate to its root

```
$ opt new <project_name> && cd <project_name>
```

2. Import a dataset from a datasource

```bash
$ opt add dataset -p <datasource_path>
Dataset with id <dataset_id> created
```

3. Using the `dataset_id` provided in the output of the `opt add dataset` command split your dataset into multiple sub-datasets in order to achive a statistically consistent evaluation.

```bash
$ opt generate subdataset <dataset_id> --by 5 --method k_fold
Subdataset with id <subdataset_id> created
```

5. Generate an approach using the `subdataset_id` provided in the provious output. 

*Tip*: Approach name can't contain whitespaces.

```
$ opt generate approach <approach_name> --subdataset <subdataset_id>
```

*Tip*: To keep consistency and optapp automation benefits don't modify the Approach class name.


8. Fill `learn`, `inference` and `parameters` methods in the recently generated approach file.
    - `learn`: Fit your model here.
    - `inference`: Make predictions here.
    - `parameters`: Declare your hyperparameters using optapp objects (`CategoricalParameter`, `IntParameter`, `FloatParameter` ...)

*Tip*: By default approach class comes decorated with `@single_run` meaning that approach ig going to run in your machine (in a single computer). More decorators are being developed such as `@dask_runner`, `@cloud_runner`, etc.

9. Run your approach using

```
$ opt run <approach_name>
```

## Running the examples

Inside the `examples/` directory you will find a folder for each example.

To run an example navigate to its directory and run the `project-setup.sh` script. Also you can check the script content in order to learn how to use the CLI.

## Generate the documentation

Using Sphinx CLI

```
$ cd docs && sphinx-build -b html source build
```

Using Makefile

```
$ cd docs && make html
```

## Check the installation

Run all unitests using the following command:

```
$ python  -m unittest test/unitests/*.py
```