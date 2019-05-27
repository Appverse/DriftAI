from abc import ABC, abstractmethod, abstractproperty

import numpy as np


class AbstractParameter(ABC):
    
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def generate_vector(self):
        """
        Generate all possible values of the parameter

        Returns
        -------
        list
            All possible values
        """
        pass

class IntParameter(AbstractParameter):
    """
    Represents an Integer parameter
    """
    def __init__(self, name, initial, limit, step):
        """
        Parameters
        ----------
        name: str
            Parameter name
        initial: int
            Start of interval. The interval includes this value
        limit: int
            End of interval. The interval does not include this value, 
            except in some cases where step is not an integer and floating point 
            round-off affects the length of out.
        setp: int
            Spacing between values.
        """
        super().__init__(name)
        self.init_value = initial
        self.limit = limit
        self.step = step
    
    def generate_vector(self):
        """
        Return evenly spaced values within a given interval
        """
        return np.arange(self.init_value, self.limit, self.step) \
                .astype(int).tolist()

class FloatParameter(AbstractParameter):
    """
    Represents an Floating parameter
    """
    def __init__(self, name, initial, limit, partitions):
        """
        Parameters
        ----------
        name: str
            Parameter name
        initial: float
            The starting value of the sequence.
        limit: float
            The end value of the sequence 
        partitions: int
            Number of samples to generate
        """
        super().__init__(name)
        self.init_value = initial
        self.limit = limit
        self.partitions = partitions
    
    def generate_vector(self):
        """
        Return evenly spaced numbers over a specified interval
        """
        return np.linspace(self.init_value, self.limit, self.partitions) \
                .astype(float).tolist()

class CategoricalParameter(AbstractParameter):
    """
    Represents a categorical parameter
    """
    def __init__(self, name, values):
        """
        Parameters
        -----------
        name: str
            Parameter name
        values: list
            Possible values
        """
        super().__init__(name)
        self.values = values
    
    def generate_vector(self):
        return self.values

class BoolParameter(AbstractParameter):
    """
    Represents a boolean parameter
    """
    def generate_vector(self):
        """
        Return the 2 only possible values for bool
        """
        return [True, False]