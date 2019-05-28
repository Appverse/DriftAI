import itertools

class ParameterGrid(object):
    """
    Responsible of generating the parameter grid.
    """

    def __init__(self, parameters):
        """
        Parameters
        ----------
        parameters: list(AbstractParameter)
        """
        self.parameters = parameters
        self.parameter_vector = self._generate_parvect()

    def _generate_parvect(self):
        """
        Creates a dictionary containing all the parameters.

        Returns
        -------
        dict
        """
        return dict([(param.name, param.generate_vector()) for param in self.parameters])

    def generate_combs(self):
        """
        Generate all possible combinations with parameters specified at the constructor
        
        Returns
        -------
        tuple(list(string), list(any))
            Tuple containing the name of parameters and all the possible combinations
        """
        combs = list(self.parameter_vector.values())
        keys = list(self.parameter_vector.keys())
        return (keys, list(itertools.product(*combs)))

    def get_parameter_count(self, param):
        """
        Counts the parameter possible values

        Parameters
        ----------
        param: str
            Name of the parameter

        Returns
        -------
        int
            Number of possible values of the parameter named <param>
        """
        return len(self.parameter_vector[param])
