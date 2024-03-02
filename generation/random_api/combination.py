import ast
import random

from generation.random_api.random_api import RandomApiGenerator
from generation.random_api.multiplication import MultiplicationGenerator
from generation.random_api.arithmetical import ArithmeticalGenerator
from generation.random_api.summation import SummationGenerator


class RandomApiCombinationGenerator(RandomApiGenerator):
    def __init__(self, summation_generator, multiplication_generator, arithmetical_generator):
        self.generators = [summation_generator,
                           multiplication_generator, arithmetical_generator]

    def get_random_generator(self):
        return random.choice(self.generators)

    def generate_flaky_function_tree(
            self,
            summation_depth,
            multiplication_depth,
            expression_depth,
            function_identifier,
            function_index,
            generator
    ):
        statements = []

        # Generate flaky function with respective generator class using the concerned parameters
        if isinstance(generator, MultiplicationGenerator):
            flaky_function = generator.generate_flaky_function_tree(
                multiplication_depth,
                f'{function_identifier}_combination_{function_index}'
            )
        if isinstance(generator, SummationGenerator):
            flaky_function = generator.generate_flaky_function_tree(
                summation_depth,
                f'{function_identifier}_combination_{function_index}'
            )
        if isinstance(generator, ArithmeticalGenerator):
            flaky_function = generator.generate_flaky_function_tree(
                expression_depth,
                f'{function_identifier}_combination_{function_index}'
            )

        statements.append(flaky_function)
        return ast.Module(statements)

    def generate_test_statements(
            self,
            summation_depth,
            multiplication_depth,
            summand,
            multiplicand,
            function_identifier,
            generator_index,
            generator
    ):
        actual = ast.Name('actual')
        expected = ast.Name('expected')
        function_statements = []

        if isinstance(generator, MultiplicationGenerator):
            actual_value = ast.Call(
                func=ast.Name(
                    f'random_api_combination.flaky_multiplication_{function_identifier}_combination_{generator_index}'),
                args=[ast.Constant(multiplicand)], keywords=[])
            function_statements.append(ast.Assign(targets=[actual], value=actual_value,
                                                  type_ignores=[]),)
            function_statements.append(ast.Assign(targets=[expected], value=ast.Constant(multiplicand ** multiplication_depth),
                                                  type_ignores=[]))
            function_statements.append(
                self.generate_assert_equality_expression(actual, expected))
        if isinstance(generator, SummationGenerator):
            actual_value = ast.Call(
                func=ast.Name(
                    f'random_api_combination.flaky_summation_{function_identifier}_combination_{generator_index}'),
                args=[ast.Constant(summand)], keywords=[])
            function_statements.append(ast.Assign(targets=[actual], value=actual_value,
                                                  type_ignores=[]),)
            function_statements.append(ast.Assign(targets=[expected], value=ast.Constant(summation_depth * summand),
                                                  type_ignores=[]))
            function_statements.append(
                self.generate_assert_equality_expression(actual, expected))
        if isinstance(generator, ArithmeticalGenerator):
            actual_value = ast.Call(
                func=ast.Name(
                    f'random_api_combination.flaky_arithmetical_{function_identifier}_combination_{generator_index}'),
                args=[], keywords=[])
            function_statements.append(ast.Assign(targets=[actual], value=actual_value,
                                                  type_ignores=[]),)
            function_statements.append(ast.Assign(targets=[expected], value=generator.arithmetical_expression,
                                                  type_ignores=[]))
            function_statements.append(
                self.generate_assert_equality_expression(actual, expected))

        return function_statements
