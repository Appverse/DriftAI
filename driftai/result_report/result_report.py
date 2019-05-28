from pathlib import Path

import sklearn
import numpy as np
import pandas as pd

from driftai.data import SubDataset
from .metrics import recall, precision, f1

class ResultReport(object):

    def __init__(self, approach, metrics):
        """
        Parameters
        ----------
        approach: driftai.Approach
            Location of the results
        metrics: array of metrics
            Set of metrics 
        """
        self.approach = approach
        self.metrics = metrics
        self.evaluation = self._calculate_metrics()


    def _get_eval_data(self):
        # Get the evaluation data from results files
        eval_results = []
        subdataset = self.approach.subdataset

        for run in self.approach.runs:
            eval_results.append({
                **run.run_parameters,
                "subdataset_set": run.subdataset_set,
                "y_true": subdataset.get_test_labels(run.subdataset_set),
                "y_pred": run.results.result
            })
        return eval_results

    def _calculate_metrics(self):
        # Calculate the metrics with the results of the current run
        eval_data = self._get_eval_data()
        eval_data_metrics = []
        for metric in self.metrics:
            for run in eval_data:
                metric_eval = metric(run["y_true"], run["y_pred"])
                run[metric.__name__] = metric_eval
                eval_data_metrics.append(run)
        return eval_data_metrics

    def as_dataframe(self):
        """
        Return the evaluations as pandas DataFrame

        Returns
        -------
        pandas.DataFrame
        """
        return pd.DataFrame(self.evaluation)
