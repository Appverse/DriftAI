class DriftAIProjectDirNotExistsException(Exception):
    def __init___(self, dErrorArguments):
        Exception.__init__(
            self,
            "Dir does not exist in current project structure: {0}".format(
                dErrorArguments))
        self.dErrorArguments = dErrorArguments


class DriftAIProjectFileNotExistsException(Exception):
    def __init___(self, dErrorArguments):
        Exception.__init__(
            self,
            "File does not exist in current project structure: {0}".format(
                dErrorArguments))
        self.dErrorArguments = dErrorArguments


class DriftAIProjectElementNotExistsException(Exception):
    def __init___(self, dErrorArgument1, dErrorArgument2):
        Exception.__init__(
            self,
            "Element {0} does not exist in current project structure: {1}".
            format(dErrorArgument1, dErrorArgument2))
        self.dErrorArgument1 = dErrorArgument1
        self.dErrorArgument2 = dErrorArgument2


class DriftAIFileDatasourceNotCompatibeException(Exception):
    def __init___(self, dErrorArgument1):
        Exception.__init__(
            self, "File format {0} not supported as Datasource".format(
                dErrorArgument1))


class DriftAIMethodNotImplementedYetException(Exception):
    def __init___(self, dErrorArgument1):
        Exception.__init__(self, "Method not implemented yet")


class DriftAIProjectNameExistsException(Exception):
    def __init___(self, dErrorArgument1):
        Exception.__init__(
            self,
            "There already exists a project in: {}".format(dErrorArgument1))


class DriftAIProjectLoadPathIsNotDirException(Exception):
    def __init___(self, dErrorArgument1):
        Exception.__init__(
            self, "The path provided is not a dir: {}".format(dErrorArgument1))


class DriftAIDatasetInfoFileDoesNotExistException(Exception):
    def __init___(self, dErrorArgument1):
        Exception.__init__(
            self,
            "Datset info file does not exist: {}".format(dErrorArgument1))


class DriftAIProjectWrongInfoFileStructureException(Exception):
    def __init___(self):
        Exception.__init__(self, "Wrong project info file structure")


class DriftAISubDatasetInfoFileWrongStructureException(Exception):
    def __init___(self):
        Exception.__init__(self, "Wrong subdataset file structure")


class DriftAISubDatasetInfoFileDoesNotExistException(Exception):
    def __init___(self, dErrorArgument1):
        Exception.__init__(
            self,
            "SubDatset info file does not exist: {}".format(dErrorArgument1))


class DriftAIRunFileWrongStructureException(Exception):
    def __init___(self):
        Exception.__init__(self, "Wrong run file structure")


class DriftAIRunFileDoesNotExistException(Exception):
    def __init___(self, dErrorArgument1):
        Exception.__init__(
            self, "Run file does not exist: {}".format(dErrorArgument1))


class DriftAIInstanceExistsException(Exception):
    def __init___(self, dErrorArgument1):
        Exception.__init__(
            self, "{} Instance already exists".format(dErrorArgument1))


class DriftAIInvalidStructureException(Exception):
    def __init___(self):
        Exception.__init__(self, "Invalid instance database structure")
