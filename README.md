# ![DriftAI Logo](img/driftailogo.png)

[![Build Status](https://travis-ci.com/Appverse/DriftAI.svg?branch=master)](https://travis-ci.com/Appverse/DriftAI)
[![Documentation Status](https://readthedocs.org/projects/driftai/badge/?version=latest)](https://driftai.readthedocs.io/en/latest/?badge=latest)

DriftAI is a Machine Learning development framework. It's main aim is to standardize the model development cycle increasing the rapidness and a higher technology flexibility, allowing the inclusion of several libraries. It establishes a common framework among developers for model reproductivity and testing.

## License

    Copyright (c) 2012 GFT Appverse, S.L., Sociedad Unipersonal.

     This Source  Code Form  is subject to the  terms of  the Appverse Public License 
     Version 2.0  ("APL v2.0").  If a copy of  the APL  was not  distributed with this 
     file, You can obtain one at <http://appverse.org/legal/appverse-license/>.

     Redistribution and use in  source and binary forms, with or without modification, 
     are permitted provided that the  conditions  of the  AppVerse Public License v2.0 
     are met.

     THIS SOFTWARE IS PROVIDED BY THE  COPYRIGHT HOLDERS  AND CONTRIBUTORS "AS IS" AND
     ANY EXPRESS  OR IMPLIED WARRANTIES, INCLUDING, BUT  NOT LIMITED TO,   THE IMPLIED
     WARRANTIES   OF  MERCHANTABILITY   AND   FITNESS   FOR A PARTICULAR  PURPOSE  ARE
     DISCLAIMED. EXCEPT IN CASE OF WILLFUL MISCONDUCT OR GROSS NEGLIGENCE, IN NO EVENT
     SHALL THE  COPYRIGHT OWNER  OR  CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT,
     INCIDENTAL,  SPECIAL,   EXEMPLARY,  OR CONSEQUENTIAL DAMAGES  (INCLUDING, BUT NOT
     LIMITED TO,  PROCUREMENT OF SUBSTITUTE  GOODS OR SERVICES;  LOSS OF USE, DATA, OR
     PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
     WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT(INCLUDING NEGLIGENCE OR OTHERWISE) 
     ARISING  IN  ANY WAY OUT  OF THE USE  OF THIS  SOFTWARE,  EVEN  IF ADVISED OF THE 
     POSSIBILITY OF SUCH DAMAGE.

## Install

1. Clone the project

```
$ git clone https://github.com/Appverse/DriftAI.git && cd driftai
```
2. You need python and pip installed. (If don't have it download it from https://www.python.org/)

3. You need Visual C++ Build Tools. Download it from https://www.microsoft.com/es-es/download/confirmation.aspx?id=48159

4. Install DriftAI with ``setup`` script.

```
$ python setup.py install
```

## Using CLI to create and run a project

1. Create a project and navigate to its root

```
$ dai new <project_name> && cd <project_name>
```

2. Import a dataset from a datasource

```bash
$ dai add dataset -p <datasource_path> 
Dataset with id <dataset_id> created
```

3. Using the `dataset_id` provided in the output of the `dai add dataset` command split your dataset into multiple sub-datasets in order to achive a statistically consistent evaluation.

```bash
$ dai generate subdataset <dataset_id> --by 5 --method k_fold
Subdataset with id <subdataset_id> created
```

5. Generate an approach using the `subdataset_id` provided in the previous output. 

*Tip*: Approach name can't contain whitespaces.

```
$ dai generate approach <approach_name> --subdataset <subdataset_id>
```

*Tip*: To keep consistency and driftai automation benefits don't modify the Approach class name.


8. Fill `learn`, `inference` and `parameters` methods in the recently generated approach file.
    - `learn`: Fit your model here.
    - `inference`: Make predictions here.
    - `parameters`: Declare your hyperparameters using driftai objects (`CategoricalParameter`, `IntParameter`, `FloatParameter` ...)

*Tip*: By default approach class comes decorated with `@single_run` meaning that approach is going to run in your machine (in a single computer). More decorators are being developed such as `@dask_runner`, `@cloud_runner`, etc.

9. Run your approach using

```
$ dai run <approach_name>
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
$ cd test/unitests
$ python  -m unittest *.py
```