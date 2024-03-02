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
            result = self.get_function_count_in_files(
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

    def get_function_count_in_files(self, directory, file_name):
        overall_function_count = 0

        for root, dirs, files in os.walk(directory):
            for file in files:
                if fnmatch.fnmatch(file, file_name):
                    file_path = os.path.join(root, file)

                    with open(file_path, 'r') as file_stream:
                        file_content = file_stream.read()

                        function_regex = re.compile(
                            r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(')
                        function_count = function_regex.findall(
                            file_content)

                        overall_function_count += len(function_count)

        return overall_function_count

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
