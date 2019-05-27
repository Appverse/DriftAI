class OptAppProjectDirNotExistsException(Exception):
    def __init___(self, dErrorArguments):
        Exception.__init__(
            self,
            "Dir does not exist in current project structure: {0}".format(
                dErrorArguments))
        self.dErrorArguments = dErrorArguments


class OptAppProjectFileNotExistsException(Exception):
    def __init___(self, dErrorArguments):
        Exception.__init__(
            self,
            "File does not exist in current project structure: {0}".format(
                dErrorArguments))
        self.dErrorArguments = dErrorArguments


class OptAppProjectElementNotExistsException(Exception):
    def __init___(self, dErrorArgument1, dErrorArgument2):
        Exception.__init__(
            self,
            "Element {0} does not exist in current project structure: {1}".
            format(dErrorArgument1, dErrorArgument2))
        self.dErrorArgument1 = dErrorArgument1
        self.dErrorArgument2 = dErrorArgument2


class OptAppFileDatasourceNotCompatibeException(Exception):
    def __init___(self, dErrorArgument1):
        Exception.__init__(
            self, "File format {0} not supported as Datasource".format(
                dErrorArgument1))


class OptAppMethodNotImplementedYetException(Exception):
    def __init___(self, dErrorArgument1):
        Exception.__init__(self, "Method not implemented yet")


class OptAppProjectNameExistsException(Exception):
    def __init___(self, dErrorArgument1):
        Exception.__init__(
            self,
            "There already exists a project in: {}".format(dErrorArgument1))


class OptAppProjectLoadPathIsNotDirException(Exception):
    def __init___(self, dErrorArgument1):
        Exception.__init__(
            self, "The path provided is not a dir: {}".format(dErrorArgument1))


class OptAppDatasetInfoFileDoesNotExistException(Exception):
    def __init___(self, dErrorArgument1):
        Exception.__init__(
            self,
            "Datset info file does not exist: {}".format(dErrorArgument1))


class OptAppProjectWrongInfoFileStructureException(Exception):
    def __init___(self):
        Exception.__init__(self, "Wrong project info file structure")


class OptAppSubDatasetInfoFileWrongStructureException(Exception):
    def __init___(self):
        Exception.__init__(self, "Wrong subdataset file structure")


class OptAppSubDatasetInfoFileDoesNotExistException(Exception):
    def __init___(self, dErrorArgument1):
        Exception.__init__(
            self,
            "SubDatset info file does not exist: {}".format(dErrorArgument1))


class OptAppRunFileWrongStructureException(Exception):
    def __init___(self):
        Exception.__init__(self, "Wrong run file structure")


class OptAppRunFileDoesNotExistException(Exception):
    def __init___(self, dErrorArgument1):
        Exception.__init__(
            self, "Run file does not exist: {}".format(dErrorArgument1))


class OptAppInstanceExistsException(Exception):
    def __init___(self, dErrorArgument1):
        Exception.__init__(
            self, "{} Instance already exists".format(dErrorArgument1))


class OptAppInvalidStructureException(Exception):
    def __init___(self):
        Exception.__init__(self, "Invalid instance database structure")
