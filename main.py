import os
import argparse
import shutil

from randomization.testsuiterandomizer import TestSuiteRandomizer
from evaluation.evaluator import get_evaluators

def main():
    for i in range(10):
        print(f'Evaluation step {i} starting ...')
        if os.path.exists('tests'):
            cleanup_old_testsuite()

        parser = argparse.ArgumentParser()
        parser.add_argument("--config_file_path")
        args = parser.parse_args()

        config_file_path = "config.json"

        if args.config_file_path:
            config_file_path = args.config_file_path

        if not os.path.exists('tests'):
            os.makedirs('tests')

        randomizer = TestSuiteRandomizer()
        randomizer.generate_randomized_test_suite(config_file_path)

        #run_test_suite()

        evaluate_test_suite()

def cleanup_old_testsuite():
    shutil.rmtree('tests')


def evaluate_test_suite():
    evaluators = get_evaluators()
    for evaluator in evaluators:
        evaluator.evaluate()


if __name__ == "__main__":
    main()
