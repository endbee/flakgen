from abc import ABC, abstractmethod
import json
import subprocess
import sys
import os


class AbstractEvaluationStrategy(ABC):
    @abstractmethod
    def evaluate(self):
        pass

    def read_report(self):
        report_path = '.report.json'
        try:
            with open(report_path) as config_file:
                report_data = json.load(config_file)
        except OSError as e:
            print(f"Unable open file \"{report_path}\": {e}", file=sys.stderr)
            sys.exit()
        return report_data

    def run_test_suite(self):
        stream = os.popen('pytest tests --json-report --verbose --random-order')
        output = stream.read()
        print(output)
