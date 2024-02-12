import fnmatch

import evaluation.strategy.abstract_evaluation_strategy
class FlakinessEvaluationStrategy(evaluation.strategy.abstract_evaluation_strategy.AbstractEvaluationStrategy):
    def evaluate(self):
        print('------------------------- Flakiness evaluation --------------------------')
        non_flaky_tests = {}
        outcomes = {}
        all_tests_are_flaky = True

        self.run_test_suite()
        report_data = self.read_report()
        for test in report_data['tests']:
            outcomes[test['nodeid']] = [test['outcome']]

        for i in range(9):
            self.run_test_suite()
            report_data = self.read_report()
            for test in report_data['tests']:
                outcomes[test['nodeid']].append(test['outcome'])

        for outcome in outcomes:
            current_outcome_flaky = self.check_passed_failed_presence(outcomes[outcome])
            if not current_outcome_flaky:
                non_flaky_tests[outcome] = outcomes[outcome]
            all_tests_are_flaky = all_tests_are_flaky and current_outcome_flaky

        if all_tests_are_flaky:
            print('All tests are flaky')
        else:
            print('Not all tests are flaky')

        count = 0
        for key in non_flaky_tests.keys():
            if 'combination' in key or 'test_state_setter' in key or key.endswith('polluter'):
                count += 1
            else:
                print(key)
        print(len(non_flaky_tests))
        print(count)

    def filter_dict_by_string(self, dictionary, substring):
        return {key: value for key, value in dictionary.items() if substring in key}

    def check_passed_failed_presence(self, arr):
        # Check if both "passed" and "failed" are present in the array
        passed_present = "passed" in arr
        failed_present = "failed" in arr

        # Return True if both are present, otherwise False
        return passed_present and failed_present

    def output_latex_table(self, data):
        data = {key: ["p" if val == "passed" else "f" for val in values] for key, values in data.items()}

        # Header
        latex_table = "\\begin{longtable}{|c|" + "|".join(["c" for _ in range(11)]) + "|}\n"
        latex_table += "\\hline\n"
        latex_table += "Viewed Test &  1 &  2 &  3 &  4 &  5 &  6 &  7 &  8 &  9 &  10 \\\\\n"
        latex_table += "\\hline\n"

        # Body
        for idx, (key, values) in enumerate(data.items()):
            display_key = self.transform_key(key)
            if all(val == "p" for val in values):
                latex_table += f"{idx}\_{display_key} & {' & '.join(values)} \\\\\n"
            elif all(val == "f" for val in values):
                latex_table += f"{idx}\_{display_key}  & {' & '.join(values)} \\\\\n"
            else:
                latex_table += f"{idx}\_{display_key} & {' & '.join(values)} \\\\\n"
            latex_table += "\\hline\n"

        # Footer
        latex_table += "\\caption{Table depicting test suite execution results for each test case, 500 test cases, 10 executions}"
        latex_table += "\\label{table:exec-res}"
        latex_table += "\\end{longtable}"

        with open("outcomes_table.txt", "w") as text_file:
            text_file.write(latex_table)

    def transform_key(self, key):
        if 'summation' in key:
            return 'rand'
        if 'arithmetical' in key:
            return 'rand\_arith'
        if 'multiplication' in key:
            return 'rand'
        if 'combination' in key:
            return 'rand\_comb'
        if key.endswith('polluter'):
            return 'order\_polluter'
        if key.endswith('state_setter') or fnmatch.fnmatch(key, '*state_setter_?'):
            return 'order\_state'

        return 'order'
