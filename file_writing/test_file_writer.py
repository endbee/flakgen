from .file_writer import FileWriter


class TestFileWriter(FileWriter):
    FILE_PATH_POSTFIX = "_test"

    # When instantiating the TestFileWrite it first writes the import-Statement that imports the functions to be tested
    def __init__(self, module_name):
        super().__init__(module_name)
        self.file_handler.write("import " + self.module_name)
        self.file_handler.write("\n")
        self.file_handler.write("\n")
        self.file_handler.write("\n")

    def get_file_path(self):
        return "testsuite/" + self.module_name + self.FILE_PATH_POSTFIX + ".py"
