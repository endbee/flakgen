from .file_writer import FileWriter


class TestFileWriter(FileWriter):
    FILE_PATH_POSTFIX = "_test"

    def get_file_path(self):
        return "tests/" + self.module_name + self.FILE_PATH_POSTFIX + ".py"
