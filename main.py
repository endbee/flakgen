import os
import astor
import argparse

from generation.generator_builder import GeneratorBuilder
from file_writing.test_file_writer import TestFileWriter
from file_writing.function_file_writer import FunctionFileWriter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file_path")
    args = parser.parse_args()

    config_file_path = "config.json"

    if args.config_file_path:
        config_file_path = args.config_file_path

    generator_builder = GeneratorBuilder(config_file_path)

    flakiness_category_generators = generator_builder.build_generator_dict()

    if not os.path.exists('testsuite'):
        os.makedirs('testsuite')

    for category in flakiness_category_generators:
        test_file_writer = TestFileWriter(category)
        function_file_writer = FunctionFileWriter(category)

        for kind in flakiness_category_generators[category]:
            generator = flakiness_category_generators[category][kind]
            func_tree = generator.generate_flaky_function_tree()
            test_tree = generator.generate_test_tree()

            test_file_writer.write_function(astor.to_source(test_tree))
            function_file_writer.write_function(astor.to_source(func_tree))

        test_file_writer.close()
        function_file_writer.close()

    run_test_suite()


def run_test_suite():
    stream = os.popen('pytest testsuite')
    output = stream.read()
    print(output)


if __name__ == "__main__":
    main()
