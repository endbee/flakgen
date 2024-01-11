from .file_writer import FileWriter


class FunctionFileWriter(FileWriter):
    FILE_PATH_POSTFIX = ""

    def get_file_path(self):
        return self.module_name + self.FILE_PATH_POSTFIX + ".py"
