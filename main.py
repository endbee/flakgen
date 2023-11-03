import ast
import os
import random

import astor
import argparse
import uuid

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

    # Instantiate generator dict that has the same structure as the config json to allow for connecting individual
    # config properties to respective generator
    flakiness_category_generators = generator_builder.build_generator_dict()

    if not os.path.exists('testsuite'):
        os.makedirs('testsuite')

    for category in flakiness_category_generators:
        # Instantiate file writer objects for each category to write them to separate file such that for example all
        # randomness functions, tests, test order dependent functions and tests are in dedicated file respectively
        test_file_writer = TestFileWriter(category)
        function_file_writer = FunctionFileWriter(category)

        # TODO: Extract module generation to dedicated function of generator
        # generate test and function pairs and write them to test.py file for each category: randomness, test order, ...
        for kind in flakiness_category_generators[category]:

            if kind == 'summation':
                generator = flakiness_category_generators[category][kind]
                test_statements = [ast.Import( names=[ast.alias('random_api')])]
                function_statements = [ast.Import( names=[ast.alias('numpy')])]
                for i in range(10):
                    identifier = uuid.uuid4().hex
                    summation_depth = random.randint(1,10)
                    summand = random.randint(1, 10)
                    func_tree = generator.generate_flaky_function_tree(summation_depth, identifier)
                    test_tree = generator.generate_test_tree(summand, summation_depth, identifier)
                    test_statements.append(test_tree)
                    function_statements.append(func_tree)

                functions_module = ast.Module(body=function_statements)
                tests_module = ast.Module(body=test_statements)
                test_file_writer.write_function(astor.to_source(tests_module))
                function_file_writer.write_function(astor.to_source(functions_module))

            if kind == 'multiplication':
                generator = flakiness_category_generators[category][kind]
                test_statements = []
                function_statements = []
                for i in range(10):
                    identifier = uuid.uuid4().hex
                    multiplication_depth = random.randint(1,10)
                    multiplicand = random.randint(1, 10)
                    func_tree = generator.generate_flaky_function_tree(multiplication_depth, identifier)
                    test_tree = generator.generate_test_tree(multiplicand, multiplication_depth, identifier)
                    test_statements.append(test_tree)
                    function_statements.append(func_tree)

                functions_module = ast.Module(body=function_statements)
                tests_module = ast.Module(body=test_statements)
                test_file_writer.write_function(astor.to_source(tests_module))
                function_file_writer.write_function(astor.to_source(functions_module))

            if kind == 'arithmetical':
                generator = flakiness_category_generators[category][kind]
                test_statements = []
                function_statements = []
                for i in range(10):
                    identifier = uuid.uuid4().hex
                    func_tree = generator.generate_flaky_function_tree(identifier)
                    test_tree = generator.generate_test_tree(identifier)
                    test_statements.append(test_tree)
                    function_statements.append(func_tree)

                functions_module = ast.Module(body=function_statements)
                tests_module = ast.Module(body=test_statements)
                test_file_writer.write_function(astor.to_source(tests_module))
                function_file_writer.write_function(astor.to_source(functions_module))

            if kind == 'basic':
                identifier = uuid.uuid4().hex
                generator = flakiness_category_generators[category][kind]
                #test_tree = generator.generate_test_tree(identifier)
                #test_file_writer.write_function(astor.to_source(test_tree))

        test_file_writer.close()
        function_file_writer.close()

    run_test_suite()


def run_test_suite():
    stream = os.popen('pytest testsuite')
    output = stream.read()
    print(output)


if __name__ == "__main__":
    main()
