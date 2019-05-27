import itertools
import warnings
from pathlib import Path
from datetime import datetime

import numpy as np

from .runs import Run
from optapp.parameters import ParameterGrid

class RunGenerator(object):
    """
    Responsible of generating runs
    """
    def __init__(self, runnable_approach):
        """
        Parameters
        ----------
        approach: RunnableApproach
            Approach containing the subdataset info and hyperparameters to generate the runs
        """
        self.creation_date = datetime.now()
        self.runnable_approach = runnable_approach
        self.extra_parameters = []

    def generate_runs(self):
        return RunGenerator.from_runnable_approach(
            self.runnable_approach, self.extra_parameters)

    @staticmethod
    def from_runnable_approach(runnable, extra_parameters=[]):
        """
        Given a runnable approach generates the runs

        Parameters
        ----------
        runnable: RunnableApproach

        Returns
        -------
        list(Run)

        """
        def get_subdataset_indices_as_parameter(subdataset):
            ind = list(subdataset.indices["sets"].keys())
            return ind

        approach = runnable.approach

        par_grid = ParameterGrid(runnable.parameters + extra_parameters)
        par_combs = par_grid.generate_combs()

        runs = []
        for par_comb in par_combs[1]:
            pars = dict(zip(par_combs[0], par_comb))
            sets = get_subdataset_indices_as_parameter(approach.subdataset)
            for s in sets:
                run = Run(subdataset=approach.subdataset, subdataset_set=s, 
                            run_parameters=pars, approach_id=approach.id)
                runs.append(run)
        return runs

    def add_parameters(self, param):
        """
        Adds an extra hyperparameter to run generator

        Parameters
        ----------
        param: AbstractParameter
        """
        self.extra_parameters.append(param)


class RunPool(object):
    """
    Pool to simplify runs iteration
    """
    def __init__(self, runs, resume=False):
        """
        Parameters
        ----------
        runs: list(Run)
            All runs to be executed
        resume: bool
            If True RunPool will only iterate through pendent|waiting runs,
            otherwise all runs will be iterated
        """
        self.iter = 0
        self.runs = runs
        self.resume = resume

    def iteruns(self):
        """
        Iterates to the pending runs

        Returns
        -------
        Run
            The next run with status equal to `waiting`
        """
        while self.has_next():

            if not self.resume or \
                self.runs[self.iter].status == "waiting" or \
                self.runs[self.iter].status == "running":
                yield self.runs[self.iter]
                self.iter += 1
            else:
                self.iter += 1

    def has_next(self):
        return self.iter < len(self.runs)
