import hashlib
import datetime
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from abc import abstractmethod, ABC, abstractproperty

from driftai.utils import maybe_make_dir, str_to_date, to_camel_case
from driftai.db import Persistent
from driftai.data import SubDataset
from driftai.run import Run
from driftai.result_report import ResultReport
from driftai.exceptions import OptAppInstanceExistsException

class Approach(Persistent):
    """
    Responsible of containg approach information as well as generate approach tree structure
    """
    
    _EMPTY_APPROACH = """
from driftai import RunnableApproach
from driftai.run import single_run

@single_run
class {}Approach(RunnableApproach):

    @property
    def parameters(self):
        \"\"\"
        Declare your parameters here
        \"\"\"
        return []

    def learn(self, data, parameters):
        \"\"\"
        Define, train and return your model here
        \"\"\"
        return None # Return a trained model

    def inference(self, model, data):
        \"\"\"
        Use the injected model to make predictions with the data
        \"\"\"
        return None  # Return the prediction

"""

    def __init__(self, project, name, subdataset=None, path=None, creation_date=None):
        """
        Parameters
        ----------
        project : Project
            DriftAI Project
        name : str
            Approach name
        subdataset: Subdataset
            DriftAI Subdataset which contains the training instances 
        path: str, optional
            Path to store the approch. Default value is <project.path>/approaches/<name>
        creation_date: str, optional
            Date of the approach creation. Should not be set manually
        """

        self.project = project
        self.name = name.replace("-", "_") # Replace - to avoid import errors
        self.subdataset = subdataset
        self.path = path or str(Path(self.project.path, "approaches"))
        self.script_path = Path(self.path, self.name + ".py")
        self.runs = []
        self.creation_date = str_to_date(creation_date) or datetime.now()
        if creation_date is None and Approach.collection().exists(self.id):
            raise OptAppInstanceExistsException("Approach")
        else:
            self.create_structure()

    @property
    def id(self):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', self.name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @staticmethod
    def collection():
        """
        Get table containing approaches

        Returns
        -------
        TinyDB instance
        """
        from driftai.db import Collections
        return Collections.approaches()
        
    def create_structure(self):
        """
        Generate approach directory structure
        """

        if not Path(self.path).exists():
            Path(self.path).mkdir()

        # Create script
        if not self.script_path.exists():
            with self.script_path.open("w") as f:
                f.write(Approach._EMPTY_APPROACH.format(to_camel_case(self.id)))

    @classmethod
    def load_from_data(cls, data):
        """
        Load approach from JSON coming from TinyDB

        Parameters
        ----------
        data: dict
            Dict containing the approach instance summary

        Returns
        --------
        Approach
            Approach instance generated from JSON data
        """
        from driftai.project import Project
        from driftai.db import Collections
        
        subdataset = Collections.subdatasets().get(data["subdataset"])
        a = Approach(
            project=Project.load(),
            name=data["name"],
            subdataset=subdataset,
            path=str(Path(data["path"]).absolute()),
            creation_date=data["creation_date"])
        
        a.runs = [Run.load_from_data(r, subdataset=subdataset) for r in data["runs"]] 
        
        return a

    @property
    def status(self):
        """
        Get the status of approach runs

        Returns
        -------
        dict
            Dictionary containing the done and left runs ... ::

            {
                "done": <are ther pendent runs?>,
                "total_runs": <all runs>,
                "done_runs": <done runs>,
                "progres_bar": <string containing the progress bar>
            }
            
        """
        total_runs = len(self.runs)
        done_runs = sum([ 1 for r in self.runs if r.done() ])

        percent = ("{}").format(int(100 * (done_runs / total_runs)))
        filledLength = int(40 * done_runs // total_runs)
        bar = "=" * filledLength + '>' + '-' * (40 - filledLength)

        return {
            "done": done_runs == total_runs,
            "total_runs": total_runs,
            "done_runs": done_runs,
            "progress_bar": " [{}] {} %".format(bar, percent)
        }
        
    def get_last_run_date(self):
        """Get the date of the last run"""

        last_date = datetime.min
        for run in self.runs:
            run.finish_date = str_to_date(run.finish_date)
            if run.done() and \
                    run.finish_date is not None and \
                    run.finish_date > last_date:

                last_date = run.finish_date

        if last_date != datetime.min:
            return last_date
        else:
            return None

    def get_info(self):
        """
        Get the info to serialize a Dataset instance

        Returns
        -------
        dict
            Dictionariy containing a Approach object summary::

            {
                "id": <unique identifier>,
                "project": <project containing the approach>,
                "subdataset": <subdataset which approach will run against>,
                "name": <approach name>,
                "path": <approach file system location>,
                "runs": <runs which runnable approach will execute>,
                "creation_date": <approach creation date>
            } 
        """
        return {
            "id": self.id,
            "project": self.project.id,
            "subdataset": self.subdataset.id,
            "name": self.name,
            "path": self.path,
            "runs": [r.get_info() for r in self.runs],
            "creation_date": str(self.creation_date)
        }


class RunnableApproach(ABC):
    """
    Object responsible to handle an approach execution 
    
    Inherit from this class in order to create your own approach and run it
    """
    def __init__(self, **kwargs):
        self.runner = kwargs["runner"]

        print("Loading approach data")
        self.approach = Approach.load(self._get_approach_id_from_class())
    
    def run(self, resume=False):
        """
        Run the approach

        Parameters
        ----------
        resume: bool
            If resume = True only pending runs will be executed, otherwise run will be generated and executed
        """
        self.runner.run(self, resume)

    def _get_approach_id_from_class(self):
        # Get id from runnable approach class
        # Example: RandomForestApproach -> random_forest
        class_name = self.__class__.__name__
        t = re.match(r"(\w+)Approach$", class_name)
        if t:
            approach_name = t.group(1)
            approach_name = re.sub("([A-Z])", r"_\1", approach_name)
            return approach_name.strip("_").lower()
        else:
            raise ValueError("Wrong class name")
                
    @property
    def parameters(self):
        """
        Define your parameters range here

        Returns
        -------
        list of AbstractParameter
            Parameters used to generate the runs
        """
        return []

    @abstractmethod
    def learn(self, parameters, data):
        """
        Define the train logic for the model here

        Returns
        -------
        any
            The trained model
        """
        pass

    @abstractmethod
    def inference(self, data):
        """
        Define the inference logic here

        Returns
        -------
        pandas.Series or numpy.array
            Containing the predicted labels
        """
        pass
