from .file_writer import FileWriter


class ClassDefinitionFileWriter(FileWriter):
    FILE_PATH_POSTFIX = "_class"

    def get_file_path(self):
        return 'tests/' + self.module_name + self.FILE_PATH_POSTFIX + ".py"
