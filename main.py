import ast
import os
import random
import string

import astor
import argparse
import uuid

from generation.generator_builder import GeneratorBuilder
from file_writing.test_file_writer import TestFileWriter
from file_writing.function_file_writer import FunctionFileWriter
from file_writing.class_definition_file_writer import ClassDefinitionFileWriter


def main():
    cleanup_old_testsuite()

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
        if category == 'random_api':
            # Instantiate file writer objects for each category to write them to separate file such that for example all
            # randomness functions, tests, test order dependent functions and tests are in dedicated file respectively


            # generate test and function pairs and write them to test.py file for each category: randomness, test order, ...
            for kind in flakiness_category_generators[category]:
                if kind == 'summation':
                    test_statements = [ast.Import(names=[ast.alias(f'{category}_{kind}')])]
                    test_file_writer = TestFileWriter(module_name=f'{category}_{kind}')
                    function_file_writer = FunctionFileWriter(module_name=f'{category}_{kind}')

                    generator = flakiness_category_generators[category][kind]
                    function_statements = [ast.Import(names=[ast.alias('numpy')])]

                    for i in range(10):
                        function_identifier = uuid.uuid4().hex
                        summation_depth = random.randint(1,10)
                        summand = random.randint(1, 10)

                        func_tree = generator.generate_flaky_function_tree(summation_depth, function_identifier)
                        test_tree = generator.generate_test_tree(summand, summation_depth, function_identifier)

                        test_statements.append(test_tree)
                        function_statements.append(func_tree)

                    functions_module = ast.Module(body=function_statements)
                    tests_module = ast.Module(body=test_statements)

                    test_file_writer.write_function(astor.to_source(tests_module))
                    function_file_writer.write_function(astor.to_source(functions_module))
                    test_file_writer.close()
                    function_file_writer.close()

                if kind == 'multiplication':
                    test_statements = [ast.Import(names=[ast.alias(f'{category}_{kind}')])]
                    test_file_writer = TestFileWriter(module_name=f'{category}_{kind}')
                    function_file_writer = FunctionFileWriter(module_name=f'{category}_{kind}')

                    function_statements = [ast.Import(names=[ast.alias('numpy')])]
                    generator = flakiness_category_generators[category][kind]

                    for i in range(10):
                        function_identifier = uuid.uuid4().hex
                        multiplication_depth = random.randint(1,5)
                        multiplicand = random.randint(1, 10)

                        func_tree = generator.generate_flaky_function_tree(multiplication_depth, function_identifier)
                        test_tree = generator.generate_test_tree(multiplicand, multiplication_depth, function_identifier)

                        test_statements.append(test_tree)
                        function_statements.append(func_tree)

                    functions_module = ast.Module(body=function_statements)
                    tests_module = ast.Module(body=test_statements)

                    test_file_writer.write_function(astor.to_source(tests_module))
                    function_file_writer.write_function(astor.to_source(functions_module))
                    test_file_writer.close()
                    function_file_writer.close()

                if kind == 'arithmetical':
                    test_statements = [ast.Import(names=[ast.alias(f'{category}_{kind}')])]
                    test_file_writer = TestFileWriter(module_name=f'{category}_{kind}')
                    function_file_writer = FunctionFileWriter(module_name=f'{category}_{kind}')

                    function_statements = [ast.Import(names=[ast.alias('numpy')])]
                    generator = flakiness_category_generators[category][kind]
                    max_expression_count = \
                        (generator_builder.data)['random_api']["arithmetical"]["max_expression_depth"]

                    for i in range(10):
                        function_identifier = uuid.uuid4().hex
                        expression_count = random.randint(1, max_expression_count)
                        func_tree = generator.generate_flaky_function_tree(expression_count, function_identifier)
                        test_tree = generator.generate_test_tree(function_identifier)

                        test_statements.append(test_tree)
                        function_statements.append(func_tree)

                    functions_module = ast.Module(body=function_statements)
                    tests_module = ast.Module(body=test_statements)

                    test_file_writer.write_function(astor.to_source(tests_module))
                    function_file_writer.write_function(astor.to_source(functions_module))
                    test_file_writer.close()
                    function_file_writer.close()

                if kind == 'combination':
                    max_multiplication_depth = \
                        (generator_builder.data)['random_api']["combination"]["multiplication"][
                            "max_multiplication_depth"]
                    max_summation_depth = \
                        (generator_builder.data)['random_api']["combination"]["summation"]["max_summation_depth"]
                    max_expression_depth = \
                        (generator_builder.data)['random_api']["combination"]["arithmetical"]["max_expression_depth"]
                    max_multiplicand = \
                        (generator_builder.data)['random_api']["combination"]["multiplication"][
                            "max_multiplicand"]
                    max_summand = \
                        (generator_builder.data)['random_api']["combination"]["summation"][
                            "max_summand"]
                    max_number_of_assertions = \
                        (generator_builder.data)['random_api']["combination"]["max_number_of_assertions"]

                    test_file_writer = TestFileWriter(module_name=f'{category}_{kind}')
                    function_file_writer = FunctionFileWriter(module_name=f'{category}_{kind}')

                    test_statements = [ast.Import(names=[ast.alias(f'{category}_{kind}')])]
                    function_statements = [ast.Import(names=[ast.alias('numpy')])]
                    generator = flakiness_category_generators[category][kind]

                    for n in range(10):
                        number_of_assertions = random.randint(1, max_number_of_assertions)
                        function_identifier = uuid.uuid4().hex
                        function_index = 0
                        test_function_statements = []

                        for i in range(number_of_assertions):
                            multiplication_depth = random.randint(1, max_multiplication_depth)
                            summation_depth = random.randint(1, max_summation_depth)
                            expression_depth = random.randint(1, max_expression_depth)
                            multiplicand = random.randint(1, max_multiplicand)
                            summand = random.randint(1, max_summand)

                            random_generator = generator.get_random_generator()

                            func_tree = generator.generate_flaky_function_tree(
                                summation_depth,
                                multiplication_depth,
                                expression_depth,
                                function_identifier,
                                function_index,
                                random_generator
                            )
                            generated_statements = generator.generate_test_statements(
                                summation_depth,
                                multiplication_depth,
                                summand,
                                multiplicand,
                                function_identifier,
                                function_index,
                                random_generator
                            )
                            test_function_statements.extend(generated_statements)
                            function_statements.append(func_tree)
                            function_index += 1

                        test_tree = ast.FunctionDef(
                                        'test_combination_' + function_identifier,
                                        ast.arguments([], [], defaults=[]),
                                        test_function_statements,
                                        []
                                    )
                        test_statements.append(test_tree)

                        functions_module = ast.Module(body=function_statements)
                        tests_module = ast.Module(body=test_statements)

                        test_file_writer.write_function(astor.to_source(tests_module))
                        function_file_writer.write_function(astor.to_source(functions_module))
                    test_file_writer.close()
                    function_file_writer.close()

        if category == 'test_order_dependent':
            for kind in flakiness_category_generators[category]:
                if kind == 'basic_victim_polluter':
                    for i in range(10):
                        file_identifier = uuid.uuid4().hex

                        test_file_writer = TestFileWriter(module_name=f'{category}_{kind}_{file_identifier}')
                        generator = flakiness_category_generators[category][kind]

                        test_tree = generator.generate_test_tree(number_of_tests=random.randint(2, 5))

                        test_file_writer.write_function(astor.to_source(test_tree))

                        test_file_writer.close()
                if kind == 'basic_brittle_state_setter':
                    for i in range(10):
                        file_identifier = uuid.uuid4().hex

                        test_file_writer = TestFileWriter(module_name=f'{category}_{kind}_{file_identifier}')
                        generator = flakiness_category_generators[category][kind]

                        test_tree = generator.generate_test_tree(states_to_be_set=random.randint(2,5))

                        test_file_writer.write_function(astor.to_source(test_tree))

                        test_file_writer.close()
                if kind == 'classes_victim_polluter':
                    for i in range(10):
                        class_identifier = uuid.uuid4().hex
                        state_identifier = random.choice(string.ascii_lowercase)
                        number_of_tests = random.randint(2, 5)

                        module_name = f'{category}_{kind}_{class_identifier}'

                        test_file_writer = TestFileWriter(module_name)
                        class_definition_file_writer = ClassDefinitionFileWriter(module_name)
                        generator = flakiness_category_generators[category][kind]

                        test_tree = generator.generate_test_tree(
                            state_identifier,
                            class_identifier,
                            number_of_tests
                        )
                        class_tree = generator.generate_class_definition(
                            class_identifier,
                            state_identifier,
                        )

                        test_file_writer.write_function(astor.to_source(test_tree))
                        class_definition_file_writer.write_function(astor.to_source(class_tree))

                        test_file_writer.close()
                        class_definition_file_writer.close()
                if kind == 'classes_brittle_state_setter':
                    for i in range(10):
                        class_identifier = uuid.uuid4().hex
                        state_identifier = random.choice(string.ascii_lowercase)
                        dummy_function_return = random.randint(0, 100)

                        module_name = f'{category}_{kind}_{class_identifier}'

                        test_file_writer = TestFileWriter(module_name)
                        class_definition_file_writer = ClassDefinitionFileWriter(module_name)
                        generator = flakiness_category_generators[category][kind]

                        test_tree = generator.generate_test_tree(
                            class_identifier,
                            state_identifier,
                            dummy_function_return
                        )
                        class_tree = generator.generate_class_definition(
                            class_identifier,
                            state_identifier,
                            dummy_function_return
                        )

                        test_file_writer.write_function(astor.to_source(test_tree))
                        class_definition_file_writer.write_function(astor.to_source(class_tree))

                        test_file_writer.close()
                        class_definition_file_writer.close()
                if kind == 'multiple_classes_victim_polluter':
                    for i in range(10):
                        module_identifier = uuid.uuid4().hex
                        class_a_identifier = uuid.uuid4().hex
                        state_a_identifier = random.choice(string.ascii_lowercase)
                        class_b_identifier = uuid.uuid4().hex
                        state_b_identifier = random.choice(string.ascii_lowercase)
                        number_of_tests = random.randint(2, 5)

                        module_name = f'{category}_{kind}_{module_identifier}'

                        test_file_writer = TestFileWriter(module_name)
                        class_definition_file_writer = ClassDefinitionFileWriter(module_name)
                        generator = flakiness_category_generators[category][kind]

                        test_tree = generator.generate_test_tree(
                            module_identifier,
                            state_a_identifier,
                            class_a_identifier,
                            state_b_identifier,
                            class_b_identifier,
                            number_of_tests
                        )

                        class_a_tree = generator.generate_class_definition(
                            class_a_identifier,
                            state_a_identifier,
                        )

                        class_b_tree = generator.generate_class_definition(
                            class_b_identifier,
                            state_b_identifier,
                        )

                        test_file_writer.write_function(astor.to_source(test_tree))
                        class_definition_file_writer.write_function(astor.to_source(class_a_tree))
                        class_definition_file_writer.write_function(astor.to_source(class_b_tree))

                        test_file_writer.close()
                        class_definition_file_writer.close()

    #run_test_suite()

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
