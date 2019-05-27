import shutil
import re
from pathlib import Path

from dependency_injector import containers, providers

from optapp.db import Database, DatabaseInjector

TEST_PATH = str(Path("test").absolute()) 
_RESOURCES_PATH = Path(TEST_PATH, "resources")

MOCK_DATASET = str(Path(_RESOURCES_PATH, "test_dataset.csv"))
IRIS_DATASET = str(Path(_RESOURCES_PATH, "Iris.csv"))

MOCK_PROJECT_NAME = "test_project_1"
MOCK_PROJECT_PATH = str(Path(TEST_PATH, MOCK_PROJECT_NAME))

MOCK_APPROACH_PATH = str(Path(TEST_PATH, "lr"))
APPROACH_EXAMPLE = str(Path(_RESOURCES_PATH, "approach_example.py"))

IRIS_APPROACH_PATH = str(Path(TEST_PATH, "dt"))
IRIS_APPROACH = str(Path(_RESOURCES_PATH, "iris_approach.py"))

DEFAULT_PROJECT_NAME = "untitled_optapp_project"

def delete_mock_projects():
    """
    Deletes the folder created or any folder starting with self.project_default_name
    """
    if Path(MOCK_APPROACH_PATH).is_dir():
        shutil.rmtree(MOCK_APPROACH_PATH)

    if Path(IRIS_APPROACH_PATH).is_dir():
        shutil.rmtree(IRIS_APPROACH_PATH)

    if Path(MOCK_PROJECT_PATH).is_dir():
        # Close database instance
        DatabaseInjector.db().close()

        # Remove the mock project
        shutil.rmtree(MOCK_PROJECT_PATH)

    for path in Path(TEST_PATH).iterdir():
        if path.is_dir():

            if path.stem.startswith(DEFAULT_PROJECT_NAME):
                DatabaseInjector.db.reset()

                # Remove default named project
                shutil.rmtree(str(path))
    
    DatabaseInjector.db.reset()

class IdentityDBInjector(containers.DeclarativeContainer):
    class DatabaseIdentity(object):
        def __init__(self, project_path):
            pass
 
        def __getattr__(self, name):
            def identity(*args):
                return args

            return identity
        
    db = providers.Singleton(DatabaseIdentity, project_path=str(Path(TEST_PATH, DEFAULT_PROJECT_NAME)))