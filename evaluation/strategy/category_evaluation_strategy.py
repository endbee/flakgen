import subprocess
import os
import re
import json
import sys
import fnmatch

import evaluation.strategy.abstract_evaluation_strategy


class CategoryEvaluationStrategy(evaluation.strategy.abstract_evaluation_strategy.AbstractEvaluationStrategy):
    def evaluate(self):
        print(f'------------------------- Category evaluation --------------------------')
        self.run_test_suite()
        report_data = self.read_report()
        config_data = self.load_config_data('config.json')
        directory_path = "tests"
        total_test_count = self.get_total_test_count(report_data)
        categories = self.get_categories()

        for category in categories:
            category_name = categories[category]['category']
            sub_category_name = categories[category]['sub_category']
            target_file_name_pattern = category_name + '_' + sub_category_name + '_*.py'
            flakiness_category = category_name + '_' + sub_category_name
            category_share = self.get_category_share(
                config_data, category_name, sub_category_name)
            result = self.count_functions_in_files(
                directory_path, target_file_name_pattern)
            print(
                f"Number of functions in {flakiness_category}: {result} target was {total_test_count*category_share}")

    def get_categories(self):
        return {
            0: {
                'category': 'random_api',
                'sub_category': 'arithmetical'
            },
            1: {
                'category': 'random_api',
                'sub_category': 'combination'
            },
            2: {
                'category': 'random_api',
                'sub_category': 'multiplication'
            },
            3: {
                'category': 'random_api',
                'sub_category': 'summation'
            },
            4: {
                'category': 'test_order_dependent',
                'sub_category': 'basic_victim_polluter'
            },
            5: {
                'category': 'test_order_dependent',
                'sub_category': 'basic_brittle_state_setter'
            },
            6: {
                'category': 'test_order_dependent',
                'sub_category': 'classes_brittle_state_setter'
            },
            7: {
                'category': 'test_order_dependent',
                'sub_category': 'classes_victim_polluter'
            },
            8: {
                'category': 'test_order_dependent',
                'sub_category': 'multiple_classes_victim_polluter'
            },
        }

    def count_functions_in_files(self, directory, file_name):
        # Initialize a counter
        total_functions = 0

        # Loop through all files in the directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                # Check if the file name matches the specified name
                if fnmatch.fnmatch(file, file_name):
                    file_path = os.path.join(root, file)

                    # Read the content of the file
                    with open(file_path, 'r') as f:
                        file_content = f.read()

                        # Use a regular expression to count functions
                        function_pattern = re.compile(
                            r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(')
                        functions_in_file = function_pattern.findall(
                            file_content)

                        # Update the total count
                        total_functions += len(functions_in_file)

        return total_functions

    def get_total_test_count(self, report_data):
        return report_data['summary']['collected']

    def get_category_share(self, config_data, category, sub_category):
        return config_data[category][sub_category]['test_number_share']

    def load_config_data(self, config_file_path):
        try:
            with open(config_file_path) as config_file:
                return json.load(config_file)
        except OSError as e:
            print(
                f"Unable open file \"{config_file_path}\": {e}", file=sys.stderr)
            sys.exit()
