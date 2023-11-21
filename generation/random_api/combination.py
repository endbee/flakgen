import ast
import random

from generation.random_api.random_api import RandomApiGenerator
from generation.random_api.multiplication import MultiplicationGenerator
from generation.random_api.arithmetical import ArithmeticalGenerator
from generation.random_api.summation import SummationGenerator




class RandomApiCombinationGenerator(RandomApiGenerator):
    def __init__(self, summation_generator, multiplication_generator, arithmetical_generator):
        self.generators = [arithmetical_generator, multiplication_generator, summation_generator]

    def get_generators(self, number_of_generators=3):
        picked_generators = []
        for i in range(number_of_generators):
            picked_generators.append(random.choice(self.generators))

        return picked_generators

    def generate_flaky_function_tree(self, max_summation_depth, max_multiplication_depth, function_identifier):
        generators = self.get_generators()
        statements = []
        function_index = 1
        multiplication_depth = random.randint(1, max_multiplication_depth)
        summation_depth = random.randint(1, max_summation_depth)

        for generator in generators:
            if isinstance(generator, MultiplicationGenerator):
                flaky_function = generator.generate_flaky_function_tree(
                    multiplication_depth,
                    f'{function_identifier}_combination_{function_index}'
                )
                statements.append(flaky_function)
            if isinstance(generator, SummationGenerator):
                flaky_function = generator.generate_flaky_function_tree(
                    summation_depth,
                    f'{function_identifier}_combination_{function_index}'
                )
                statements.append(flaky_function)
            if isinstance(generator, ArithmeticalGenerator):
                flaky_function = generator.generate_flaky_function_tree(
                    multiplication_depth,
                    f'{function_identifier}_combination_{function_index}'
                )
                statements.append(flaky_function)
            function_index += 1

        return ast.Module(statements)

    def generate_test_tree(self, function_identifier):
        statements = []
        return ast.Module(statements)
