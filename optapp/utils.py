import os
import re
import pathlib
from urllib.parse import urlparse
from pathlib import Path
from datetime import datetime

def maybe_make_dir(path):
    """
    Creates a directory if it does not exist

    Parameters
    ----------
    path : pathlib.Path
        Directory path
    """
    if not path.is_dir():
        path.mkdir()


def import_from(module, name):
    """
    Imports an attribute from a module.

    Parameters
    ----------
    module : str
        Module namespace. For example: sklearn.model_selection
    name : str
        Name of attribute. For example train_test_split

    Returns
    -------
    any
        Attribute if found else None

    """
    module = __import__(module, fromlist=[name])
    return getattr(module, name)

def get_current_project_db(path):
    """ 
    Get project database
    
    Parameters
    ----------
    path: str
        Any path inside optapp project
    
    Returns
    -------
    optapp.db.Database

    """
    from optapp.db import Database

    def _inspect_path(path):
        project_db_file = Path(path, "optapp.db")
        if project_db_file.exists():
            return Database(project_db_file.parent)
        return None

    current_path = Path(path).absolute()
    root = False
    last_len = 0
    while not root:
        project_db = _inspect_path(current_path)
        
        if project_db is not None:
            return project_db
        
        current_path = current_path.parent
        root = len(str(current_path)) == last_len
        last_len = len(str(current_path))
    
    return project_db


def check_folder_structure(path_to_dir, content_dict, exception_dict):
    """
    Check if the directory structure is the expected. 
    In case folder structure is invalid raises the exception specified inside `exception_dict`

    Parameters
    ----------
    path_to_dir : str
        Directory path
    path_to_dir : dict
        Dictionary which its keys are the expected contents, 
        and its values are the contents' file type (file | dir)
    exception_dict : dict
        Dictionary containing the exceptions to be thrown in case a file or a directory is missing
    
    """
    contents = [p.name for p in Path(path_to_dir).iterdir()]

    for element in content_dict.keys():
        if element in contents:
            if content_dict[element] == "file":
                if not Path(path_to_dir, element).exists():
                    raise exception_dict["file"]
            elif content_dict[element] == "dir":
                if not Path(path_to_dir, element).is_dir():
                    raise exception_dict["dir"]
        else:
            raise exception_dict["default"](element, path_to_dir)


def filepath_to_uri(filepath):
    """
    Converts a system path to an uri file

    Parameters
    ----------
    filepath: str
        Path to be converted

    Example
    -------
    filepath_to_uri(/home/my_file.txt) -> file:///home/myfile.txt
    """

    return Path(filepath).absolute().as_uri()


def check_uri(uri):
    """ Checks if a string is an uri

    Parameters
    ------
    uri: str
        String to be tested

    Returns
    -------
    bool
        True -> If uri is an uri
        False -> If uri is not an uri
    """
    uri = urlparse(uri)
    accepted_schemes = ['file', 'http', 'https']
    return uri.scheme in accepted_schemes


def uri_to_filepath(uri):
    """ 
    Transforms a file uri to path system

    Parameters
    ----------
    uri: str
        String to be transformed

    Returns
    -------
    str
        Converted string

    Example
    -------
    uri_to_filepath("file:///home/myfile.txt") -> /home/myfile.txt

    """
    if check_uri(uri):
        parsed_uri = urlparse(uri)
        if parsed_uri.scheme == "file":
            mod_path = parsed_uri.path

            # TODO: Ugly but necessary for windows
            if mod_path.startswith("/C:"):
                mod_path = mod_path[1:]
            return mod_path
    return None


def get_file_extension(filename):
    """ 
    Returns the file extension without the dot

    Parameters
    ----------
    filename: str
        Path to file

    Returns
    -------
    str
        File extension without the '.' 
    """
    return Path(filename).suffix.replace(".", "")


def str_to_date(in_str):
    """ 
    Converts a string date to datetime. 
    If the parameter is a `datetime` returns it without any transformation else
    if the parameter is a string casts it to a `datetime` with the following format: %Y-%m-%d %H:%M:%S.%f
    Parameters
    ----------
    in_str: str or datetime
        String to be casted as datetime

    Returns
    -------
    datetime
        Casted string
    """
    if in_str is None:
        return None
        
    if isinstance(in_str, str):
        try:
            dd = datetime.strptime(in_str, "%Y-%m-%d %H:%M:%S.%f")
            return dd
        except ValueError:
            return None
    elif isinstance(in_str, datetime):
        return in_str
    

def print_progress_bar(iteration, total, prefix = '', suffix = ''):
    """
    Call in a loop to create terminal progress bar
    
    Parameters
    ----------
    iteration: int
        Current iteration
    total: int
        Total iterations
    prefix: str
        Prefix string
    suffix: str
        Suffix string
    """
    percent = ("{}").format(int(100 * (iteration / total)))
    filledLength = int(40 * iteration // total)
    bar = "=" * filledLength + '>' + '-' * (40 - filledLength)
    print('\r%s [%s] %s %% %s' % (prefix, bar, percent, suffix), end = '\r')

    # Print New Line on Complete
    if iteration == total: 
        print()

def compile_path_pattern(p, basepattern="", all_path_matcher_name=''):
    """
    Convert a pattern expression for the data path to regular expression
    
    Parameters
    ----------
    p: str
        Path pattern expression. Example: '{testset}/{class}_{}.png|jpg'
    basepattern: str
        Base pattern. This is a fixed part of the pattern (like the root path)
    all_path_matcher_name: str
        Name to name the group matching to all path pattern expression: 
        Example ::

            >>> regex = compile_path_pattern('{testset}/{class}/{}.png|jpg',
            ... basepattern="/home/users/, all_path_matcher_name='file')
            >>> g = re.match(regex, '/home/users/train/0/0.png')
            >>> print(g)
            {
                ...
                'file': 'train/0/0.png'
                ...
            }

    """

    os_p = p.replace('/', os.path.sep)
    #split extension
    try:
        extension = os_p.split(".")[1]
    except ValueError:
        extension = None
    if extension:
        #check if single
        t = re.match("\w+",extension)
        if t:
            extension_list = [extension]
        #check if multiple
        g = re.match("\[((\w+[|]?)+)\]",extension)
        if g:
            extension_list = g.group(1).split("|")
        if t is None and g is None:
            raise Exception("extension not matched")
    else:
        extension_list = ["\w+"]
    
    #create parsed extension
    if len(extension_list) == 1:
        parsed_extension = ".{}".format(extension_list[0])
    else:
        extensions_join = "|".join(extension_list)
        expr = "(:?{})".format(extensions_join) 
        parsed_extension = ".{}".format(expr)

    #split path
    try:
        path = os_p.split(".")[0]
    except ValueError:
        path = None

    if path:
        parsed_path = re.sub(r'{(\w+)}',r'(?P<\1>[a-zA-z0-9]+)', path)
        parsed_path = re.sub(r'{}',r'[a-zA-z0-9]+', parsed_path)
    
    if not all_path_matcher_name:
        compiled_expr = basepattern + \
                        os.path.sep + \
                        "{}{}".format(parsed_path,
                                      parsed_extension)
    else:
        compiled_expr = basepattern + \
                        os.path.sep + \
                        r"(?P<{}>{}{})".format(all_path_matcher_name, 
                                               parsed_path, 
                                               parsed_extension)


    return compiled_expr.encode('unicode-escape').decode()

def to_camel_case(str_name, separator_values=['-', '_']):
    """
    Converts an string to camel case naming convention

    Parameters
    ----------
    str_name: str
        String to be converted
    separator_values: list of str, optional
        String separators
    
    Returns
    -------
    str
        String in camel case format

    Example
    -------
    to_camel_case('random_forest', spearator_values=['_']) -> RandomForest
    """
    camel_case = str_name
    for sep in separator_values:
        camel_case = camel_case.replace(sep, " ")

    return camel_case.title().replace(" ", "")