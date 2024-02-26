from .file_writer import FileWriter


class FunctionFileWriter(FileWriter):
    FILE_PATH_POSTFIX = ""

    def get_file_path(self):
        file_path_prefix = 'tests/'

        if (self.is_evaluation):
            file_path_prefix = ''

        return file_path_prefix + self.module_name + self.FILE_PATH_POSTFIX + ".py"
