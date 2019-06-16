from abc import ABC, abstractmethod
from pathlib import Path
import warnings

from .run_manage import RunPool, RunGenerator
from driftai.result_report import Result
from driftai.utils import print_progress_bar
from driftai.logger import DriftAILogger

import numpy as np

class AbstractRunner(ABC):
    def __init__(self):
        self.logger = DriftAILogger()

    @abstractmethod
    def run(self, approach, resume=False):
        """
        Runs an approach
        """
        pass

class SingleRunner(AbstractRunner):
    """
    Runs an approach in a single machine
    """

    def _load_runs(self, runnable_approach, resume):
        if not resume:
            # Remove old runs
            self.logger.info("Removing previous runs...")
            runnable_approach.approach.runs.clear()
            runnable_approach.approach.update()
            
            self.logger.info("Generating runs...")
            runs = RunGenerator.from_runnable_approach(runnable_approach)
            runnable_approach.approach.runs = runs

            self.logger.info("Saving new runs...")
            runnable_approach.approach.update()
        else: 
            self.logger.info("Resuming runs...")
            self.logger.debug("Reading runs...")
            runs = runnable_approach.approach.runs
        return runs

    def run(self, runnable_approach, resume=False):
        # Generate or load the runs
        runs = self._load_runs(runnable_approach, resume)

        if len(runs) == 0:
            self.logger.warning("Cannot load runs. Did you generated them?")
            return

        # Count finished and left runs
        n_done_runs = len([r for r in runs if r.status == "finished"])
        n_left_runs = len(runs) - n_done_runs

        # If resume is True and there aren't runs to run warn the user
        if resume and n_left_runs == 0:
            self.logger.warning("All runs are finished. Regenerate the runs or run with resume=False")
            return

        self.logger.info("Running...")
        
        # Print on 10% completition
        log_every = (len(runs) * 10) // 100
        log_every = log_every or 1

        print_progress_bar(n_done_runs, len(runs))
        
        # Execute the runs
        for run in RunPool(runs, resume).iteruns():
            run.status = "running"
            run.update()

            # Get the data which will be using to train and validate
            train_data = run.get_train_data()
            test_data = run.get_test_data()
            parameters = run.run_parameters
            
            # Fit and inference
            model = runnable_approach.learn(train_data, parameters)
            predictions = runnable_approach.inference(model, test_data)
            
            # Convert predictions to python list in order to serialize them
            if isinstance(predictions, np.ndarray):
                predictions = predictions.tolist()   

            # Set the results and store them
            run.results = Result(None, result=predictions)
            run.update()

            # Update the progress bar
            n_done_runs += 1
            print_progress_bar(n_done_runs, len(runs))
            
            if n_done_runs % log_every == 0:
                self.logger.debug('{}/{} runs executed.'.format(n_done_runs, len(runs)))


class DaskRunner(AbstractRunner):
    """
    Runs an approach in a single machine using dask parallelization
    """
    def run(self, approach, resume=False):
        # TODO: See test/resources/my_run_dask.py
        pass

class CloudRunner(AbstractRunner):
    """
    Runs an approach in a single machine using dask parallelization
    """
    def run(self, approach, resume=False):
        # TODO: See test/resources/my_run_dask.py
        pass
