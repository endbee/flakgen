from .file_writer import FileWriter


class TestFileWriter(FileWriter):
    FILE_PATH_POSTFIX = "_test"

    def __init__(self, module_name):
        super().__init__(module_name)


    def get_file_path(self):
        return "tests/" + self.module_name + self.FILE_PATH_POSTFIX + ".py"
