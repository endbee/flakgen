import ast

from generation.generator import Generator


# Base generator class for all classes that generate flaky function and test case pairs (of different kinds) due to randomness
class RandomApiGenerator(Generator):

    # Generates function call like 'numpy.random.random()'
    @staticmethod
    def generate_random_float_number_expression():
        return ast.Call(ast.Attribute(value=ast.Name(id='numpy.random'), attr='random'), args=[], keywords=[])
