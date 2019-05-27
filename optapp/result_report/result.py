from datetime import datetime
from pathlib import Path

from optapp.utils import str_to_date

class Result(object):
    """
    Object responsible of containing the results obtained by an specific run
    """
    def __init__(self, time, result=None, date=datetime.now()):
        """
        Parameters
        ----------
        time: int
            Elapsed time of the run
        result: list, np.array, pandas.Series
            The labels predicted by the approach
        run: Run
            This Run that has generated the results
        date: datetime, str, optional
            Creation date. Should not be set manually
        """
        self.date = str_to_date(date)
        self.time = time
        self.result = result

    def get_info(self):
        """
        Get a summary of a result instance

        Returns
        -------
        dict
            Dict containing essential data of result::

            {
                "date": <creation_date>,
                "time": timem
                "result": dict containing the metrics and its value
            }
        """
        return {
            "date": str(self.date),
            "time": self.time,
            "result": self.result
        }