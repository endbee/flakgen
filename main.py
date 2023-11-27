import os
import argparse

from randomization.randomizer import Randomizer

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

    randomizer = Randomizer()
    randomizer.generateRandomizedTestSuite(config_file_path)

    run_test_suite()

def cleanup_old_testsuite():
    stream = os.popen('rm -rf testsuite')
    output = stream.read()
    print(output)


def run_test_suite():
    stream = os.popen('pytest testsuite --random-order')
    output = stream.read()
    print(output)


if __name__ == "__main__":
    main()
