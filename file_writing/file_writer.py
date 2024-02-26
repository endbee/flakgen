from abc import ABC, abstractmethod
import sys


class FileWriter(ABC):

    # Opens respective file for writing for the module
    def __init__(self, module_name, is_evaluation=False):
        self.module_name = module_name
        self.is_evaluation = is_evaluation

        try:
            self.file_handler = open(self.get_file_path(), "w")
        except OSError as e:
            print(
                f"Unable to open file \"{self.get_file_path()}\": {e}", file=sys.stderr)
            sys.exit()

    # Gets a function definition as string and writes it to the file
    def write_function(self, function):
        self.file_handler.write(function)
        self.file_handler.write("\n")
        self.file_handler.write("\n")

    @abstractmethod
    def get_file_path(self):
        pass

    def close(self):
        self.file_handler.close()
