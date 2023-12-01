import os
import argparse
import shutil

from randomization.testsuiterandomizer import TestSuiteRandomizer

def main():
    cleanup_old_testsuite()

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file_path")
    args = parser.parse_args()

    config_file_path = "config.json"

    if args.config_file_path:
        config_file_path = args.config_file_path

    if not os.path.exists('testsuite'):
        os.makedirs('testsuite')

    randomizer = TestSuiteRandomizer()
    randomizer.generate_randomized_test_suite(config_file_path)

    run_test_suite()

def cleanup_old_testsuite():
    shutil.rmtree('testsuite')

def run_test_suite():
    stream = os.popen('pytest testsuite --random-order')
    output = stream.read()
    print(output)


if __name__ == "__main__":
    main()
