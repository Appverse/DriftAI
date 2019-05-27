import functools
from .runner import SingleRunner

def single_run(cls):
    """
    Injects a SingleRunner to a RunnableApproach class
    """
    @functools.wraps(cls)
    def wrapper_single_run(*args, **kwargs):
        return cls(runner=SingleRunner(), **kwargs)
    return wrapper_single_run