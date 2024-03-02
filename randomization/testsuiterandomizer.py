import ast
import random
import string
import astor
import uuid
import sys

from generation.generator_builder import GeneratorBuilder
from file_writing.test_file_writer import TestFileWriter
from file_writing.function_file_writer import FunctionFileWriter
from file_writing.class_definition_file_writer import ClassDefinitionFileWriter

class TestSuiteRandomizer():
    def generate_randomized_test_suite(self, config_file_path):
        generator_builder = GeneratorBuilder(config_file_path)
        config_data = generator_builder.config_data

        # Instantiate generator dict that has the same structure as the config json to allow for connecting individual
        # config properties to respective generator
        flakiness_category_generators = generator_builder.build_generator_dict()

        self.assert_test_shares_add_to_one(config_data, flakiness_category_generators)

        max_total_test_count = config_data['max_total_test_count']
        min_total_test_count = config_data['min_total_test_count']
        total_test_count = random.randint(min_total_test_count, max_total_test_count)

        for category in flakiness_category_generators:

            # generate test and function pairs (called test_suites in following, since they can be standalone)
            # and write them to test.py file for each category: randomness, test order, ...
            for kind in flakiness_category_generators[category]:
                if kind == 'summation':
                    self.generate_randomized_random_api_summation_test_suite(
                        category,
                        config_data,
                        flakiness_category_generators,
                        kind,
                        total_test_count
                    )

                if kind == 'multiplication':
                    self.generate_randomized_random_api_multiplication_test_suite(
                        category,
                        config_data,
                        flakiness_category_generators,
                        kind,
                        total_test_count
                    )

                if kind == 'arithmetical':
                    self.generate_randomized_random_api_arithmetical_test_suite(
                        category,
                        config_data,
                        flakiness_category_generators,
                        kind,
                        total_test_count
                    )

                if kind == 'combination':
                    self.generate_randomized_random_api_combination_test_suite(
                        category,
                        config_data,
                        flakiness_category_generators,
                        kind,
                        total_test_count
                    )

                if kind == 'basic_victim_polluter':
                    self.generate_randomized_test_order_dependent_basic_victim_polluter_test_suite(
                        category,
                        flakiness_category_generators,
                        kind,
                        config_data,
                        total_test_count
                    )

                if kind == 'basic_brittle_state_setter':
                    self.generate_randomized_test_order_dependent_basic_brittle_state_setter_test_suite(
                        category,
                        flakiness_category_generators,
                        kind,
                        config_data,
                        total_test_count
                    )

                if kind == 'classes_victim_polluter':
                    self.generate_randomized_test_order_dependent_classes_victim_polluter_test_suite(
                        category,
                        flakiness_category_generators,
                        kind,
                        config_data,
                        total_test_count
                    )

                if kind == 'classes_brittle_state_setter':
                    self.generate_randomized_test_order_dependent_classes_brittle_state_setter_test_suite(
                        category,
                        flakiness_category_generators,
                        kind,
                        config_data,
                        total_test_count
                    )

                if kind == 'multiple_classes_victim_polluter':
                    self.generate_randomized_test_order_dependent_multiple_classes_victim_polluter_test_suite(
                        category,
                        config_data,
                        flakiness_category_generators,
                        kind,
                        total_test_count
                    )

                if kind == 'task_race_cond':
                    self.generate_randomized_async_wait_task_race_cond_test_suite(
                        category,
                        config_data,
                        flakiness_category_generators,
                        kind,
                        total_test_count
                    )

    def generate_randomized_test_order_dependent_multiple_classes_victim_polluter_test_suite(
            self,
            category,
            config_data,
            flakiness_category_generators,
            kind,
            total_test_count
    ):
        relative_tests_share = config_data[category][kind]['test_number_share']
        tests_share = int(total_test_count * relative_tests_share)

        generated_tests = 0
        max_class_count = \
            (config_data)['test_order_dependent']["multiple_classes_victim_polluter"][
                "max_class_count"]

        # Ensure that the correct number of tests is generated
        while generated_tests < tests_share:
            module_identifier = uuid.uuid4().hex

            class_count = random.randint(1, max_class_count)
            class_state_identifiers_map = {}

            for n in range(class_count):
                class_identifier = uuid.uuid4().hex
                state_identifier = random.choice(string.ascii_lowercase)
                class_state_identifiers_map[class_identifier] = state_identifier

            number_of_tests = random.randint(2, 5)

            # Handle test number edge case where randomly picked test count would lead to generating more test cases
            # as intended
            if (generated_tests + number_of_tests) > tests_share:
                number_of_tests = tests_share - generated_tests

            generated_tests += number_of_tests

            module_name = f'{category}_{kind}_{module_identifier}'

            test_file_writer = TestFileWriter(module_name)
            class_definition_file_writer = ClassDefinitionFileWriter(module_name)
            generator = flakiness_category_generators[category][kind]

            test_tree = generator.generate_test_tree(
                module_identifier,
                class_state_identifiers_map,
                number_of_tests
            )

            classes_tree = generator.generate_class_definitions(
                class_state_identifiers_map
            )

            test_file_writer.write_function(astor.to_source(test_tree))
            class_definition_file_writer.write_function(astor.to_source(classes_tree))

            test_file_writer.close()
            class_definition_file_writer.close()

    def generate_randomized_test_order_dependent_classes_brittle_state_setter_test_suite(
            self,
            category,
            flakiness_category_generators,
            kind,
            config_data,
            total_test_count
    ):
        relative_tests_share = config_data[category][kind]['test_number_share']
        tests_share = int(total_test_count * relative_tests_share)

        generated_tests = 0

        # Ensure that the correct number of tests is generated
        while generated_tests < tests_share:
            class_identifier = uuid.uuid4().hex
            state_identifier = random.choice(string.ascii_lowercase)
            dummy_function_return = random.randint(0, 100)

            generated_tests += 2

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

    def generate_randomized_test_order_dependent_classes_victim_polluter_test_suite(
            self,
            category,
            flakiness_category_generators,
            kind,
            config_data,
            total_test_count
    ):
        relative_tests_share = config_data[category][kind]['test_number_share']
        tests_share = int(total_test_count * relative_tests_share)

        generated_tests = 0

        # Ensure that the correct number of tests is generated
        while generated_tests < tests_share:
            class_identifier = uuid.uuid4().hex
            state_identifier = random.choice(string.ascii_lowercase)
            number_of_tests = random.randint(2, 5)

            if (generated_tests + number_of_tests) > tests_share:
                number_of_tests = tests_share - generated_tests

            generated_tests += number_of_tests

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

    def generate_randomized_test_order_dependent_basic_brittle_state_setter_test_suite(
            self,
            category,
            flakiness_category_generators,
            kind,
            config_data,
            total_test_count
    ):
        relative_tests_share = config_data[category][kind]['test_number_share']
        # we have to divide by two because becuause for each state to be set there are always 2 tests generated
        tests_share = int(int(total_test_count * relative_tests_share)/2)

        generated_tests = 0

        # Ensure that the correct number of tests is generated
        while generated_tests < tests_share:
            number_of_tests = random.randint(2, 5)

            if (generated_tests + number_of_tests) > tests_share:
                number_of_tests = tests_share - generated_tests

            generated_tests += number_of_tests
            file_identifier = uuid.uuid4().hex

            test_file_writer = TestFileWriter(module_name=f'{category}_{kind}_{file_identifier}')
            generator = flakiness_category_generators[category][kind]

            test_tree = generator.generate_test_tree(states_to_be_set=number_of_tests)

            test_file_writer.write_function(astor.to_source(test_tree))

            test_file_writer.close()

    def generate_randomized_test_order_dependent_basic_victim_polluter_test_suite(
            self,
            category,
            flakiness_category_generators,
            kind,
            config_data,
            total_test_count
    ):
        relative_tests_share = config_data[category][kind]['test_number_share']
        tests_share = int(total_test_count * relative_tests_share)

        generated_tests = 0

        # Ensure that the correct number of tests is generated
        while generated_tests < tests_share:
            number_of_tests = random.randint(2, 5)

            if (generated_tests + number_of_tests) > tests_share:
                number_of_tests = tests_share - generated_tests

            generated_tests +=  number_of_tests
            file_identifier = uuid.uuid4().hex

            test_file_writer = TestFileWriter(module_name=f'{category}_{kind}_{file_identifier}')
            generator = flakiness_category_generators[category][kind]

            test_tree = generator.generate_test_tree(number_of_tests=number_of_tests)

            test_file_writer.write_function(astor.to_source(test_tree))

            test_file_writer.close()

    def generate_randomized_random_api_combination_test_suite(
            self,
            category,
            config_data,
            flakiness_category_generators,
            kind,
            total_test_count
    ):
        max_multiplication_depth = \
            (config_data)['random_api']["combination"]["multiplication"][
                "max_multiplication_depth"]
        max_summation_depth = \
            (config_data)['random_api']["combination"]["summation"]["max_summation_depth"]
        max_expression_depth = \
            (config_data)['random_api']["combination"]["arithmetical"][
                "max_expression_depth"]
        max_multiplicand = \
            (config_data)['random_api']["combination"]["multiplication"][
                "max_multiplicand"]
        max_summand = \
            (config_data)['random_api']["combination"]["summation"][
                "max_summand"]
        max_number_of_assertions = \
            (config_data)['random_api']["combination"]["max_number_of_assertions"]
        relative_tests_share = config_data[category][kind]['test_number_share']
        tests_share = int(total_test_count * relative_tests_share)


        test_file_writer = TestFileWriter(module_name=f'{category}_{kind}')
        function_file_writer = FunctionFileWriter(module_name=f'{category}_{kind}')

        test_statements = [ast.Import(names=[ast.alias(f'{category}_{kind}')])]
        function_statements = [ast.Import(names=[ast.alias('numpy')])]

        generator = flakiness_category_generators[category][kind]

        # Ensure that the correct number of tests is generated
        for n in range(tests_share):
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
            test_statements = []
            function_statements = []
        test_file_writer.close()
        function_file_writer.close()

    def generate_randomized_random_api_arithmetical_test_suite(
            self,
            category,
            config_data,
            flakiness_category_generators,
            kind,
            total_test_count
    ):
        test_file_writer = TestFileWriter(module_name=f'{category}_{kind}')
        function_file_writer = FunctionFileWriter(module_name=f'{category}_{kind}')

        function_statements = [ast.Import(names=[ast.alias('numpy')])]
        test_statements = [ast.Import(names=[ast.alias(f'{category}_{kind}')])]

        generator = flakiness_category_generators[category][kind]

        max_expression_count = \
            (config_data)['random_api']["arithmetical"]["max_expression_depth"]
        relative_tests_share = config_data[category][kind]['test_number_share']
        tests_share = int(total_test_count * relative_tests_share)

        # Ensure that the correct number of tests is generated
        for i in range(tests_share):
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

    def generate_randomized_random_api_multiplication_test_suite(
            self,
            category,
            config_data,
            flakiness_category_generators,
            kind,
            total_test_count
    ):
        test_statements = [ast.Import(names=[ast.alias(f'{category}_{kind}')])]
        test_file_writer = TestFileWriter(module_name=f'{category}_{kind}')
        function_file_writer = FunctionFileWriter(module_name=f'{category}_{kind}')

        max_multiplication_depth = \
            (config_data)['random_api']["multiplication"]["max_multiplication_depth"]
        max_multiplicand = \
            (config_data)['random_api']["multiplication"]["max_multiplicand"]
        relative_tests_share = config_data[category][kind]['test_number_share']
        tests_share = int(total_test_count * relative_tests_share)

        function_statements = [ast.Import(names=[ast.alias('numpy')])]
        generator = flakiness_category_generators[category][kind]

        # Ensure that the correct number of tests is generated
        for i in range(tests_share):
            function_identifier = uuid.uuid4().hex
            multiplication_depth = random.randint(1, max_multiplication_depth)
            multiplicand = random.randint(1, max_multiplicand)

            func_tree = generator.generate_flaky_function_tree(multiplication_depth,
                                                               function_identifier)
            test_tree = generator.generate_test_tree(multiplicand, multiplication_depth,
                                                     function_identifier)

            test_statements.append(test_tree)
            function_statements.append(func_tree)
        functions_module = ast.Module(body=function_statements)
        tests_module = ast.Module(body=test_statements)
        test_file_writer.write_function(astor.to_source(tests_module))
        function_file_writer.write_function(astor.to_source(functions_module))
        test_file_writer.close()
        function_file_writer.close()

    def generate_randomized_random_api_summation_test_suite(
            self,
            category,
            config_data,
            flakiness_category_generators,
            kind,
            total_test_count
    ):
        test_statements = [ast.Import(names=[ast.alias(f'{category}_{kind}')])]
        test_file_writer = TestFileWriter(module_name=f'{category}_{kind}')
        function_file_writer = FunctionFileWriter(module_name=f'{category}_{kind}')

        relative_tests_share = config_data[category][kind]['test_number_share']
        tests_share = int(total_test_count * relative_tests_share)

        max_summation_depth = \
            (config_data)['random_api']["summation"]["max_summation_depth"]
        max_summand = \
            (config_data)['random_api']["summation"]["max_summand"]
        generator = flakiness_category_generators[category][kind]
        function_statements = [ast.Import(names=[ast.alias('numpy')])]

        # Ensure that the correct number of tests is generated
        for i in range(tests_share):
            function_identifier = uuid.uuid4().hex
            summation_depth = random.randint(1, max_summation_depth)
            summand = random.randint(1, max_summand)

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

    def generate_randomized_async_wait_task_race_cond_test_suite(
            self,
            category,
            config_data,
            flakiness_category_generators,
            kind,
            total_test_count
    ):
        relative_tests_share = config_data[category][kind]['test_number_share']
        tests_share = int(total_test_count * relative_tests_share)

        generator = flakiness_category_generators[category][kind]

        # Ensure that the correct number of tests is generated
        for i in range(tests_share):
            test_statements = []

            function_identifier = uuid.uuid4().hex

            test_file_writer = TestFileWriter(module_name=f'{category}_{kind}_{function_identifier}')

            states = list(range(1, 1001))

            init_state = random.choice(states)
            states.remove(init_state)
            failure_state = random.choice(states)
            states.remove(failure_state)
            success_state = random.choice(states)
            states.remove(success_state)

            test_statements.extend(generator.generate_imports())
            test_statements.append(generator.generate_state_init(init_state))
            test_statements.extend(generator.generate_delay_init())
            test_statements.append(generator.generate_success_state_setter_func(success_state, function_identifier))
            test_statements.append(generator.generate_failure_state_setter_func(failure_state, function_identifier))
            test_tree = generator.generate_test_tree(function_identifier, success_state)

            test_statements.append(test_tree)

            tests_module = ast.Module(body=test_statements)
            test_file_writer.write_function(astor.to_source(tests_module))
            test_file_writer.close()

    def assert_test_shares_add_to_one(self, config_data, flakiness_category_generators):
        total_test_number_share = 0
        for category in flakiness_category_generators:
            for kind in flakiness_category_generators[category]:
                total_test_number_share += config_data[category][kind]['test_number_share']

        if total_test_number_share != 1 :
            print(f'Test number share does not add up to 1, instead: {total_test_number_share}', file=sys.stderr)
            sys.exit()