from abc import ABC, abstractmethod
import sys


class FileWriter(ABC):
    def __init__(self, module_name):
        self.module_name = module_name

        try:
            self.file_handler = open(self.get_file_path(), "w")
        except OSError as e:
            print(f"Unable to open file \"{self.get_file_path()}\": {e}", file=sys.stderr)
            sys.exit()

        self.file_handler.write("import " + module_name)
        self.file_handler.write("\n")
        self.file_handler.write("\n")
        self.file_handler.write("\n")

    def write_function(self, function):
        self.file_handler.write(function)
        self.file_handler.write("\n")
        self.file_handler.write("\n")

    @abstractmethod
    def get_file_path(self):
        pass

    def close(self):
        self.file_handler.close()
