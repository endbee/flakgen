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
            current_outcome_flaky = self.check_passed_failed_presence(
                outcomes[outcome])
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

    def check_passed_failed_presence(self, arr):
        # Check if both "passed" and "failed" are present in the array
        passed_present = "passed" in arr
        failed_present = "failed" in arr

        # Return True if both are present, otherwise False
        return passed_present and failed_present
