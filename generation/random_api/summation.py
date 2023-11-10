import ast

from generation.random_api.random_api import RandomApiGenerator


class SummationGenerator(RandomApiGenerator):
    def __init__(self, flakiness_prob):
        self.flakiness_prob = flakiness_prob

    # Generates function that adds a summand as often as summation_depth indicates and then adds a noise with some prob
    # like summation_depth=3, summand=5: 5 + 5 + 5 or 5 + 5 + 5 + 0.1
    def generate_flaky_function_tree(self, summation_depth, function_identifier):
        epsilon = ast.Constant(0.1)
        zero = ast.Constant(0)

        if_expr = ast.IfExp(
            self.generate_compare_lt_expression(self.generate_random_float_number_expression(), ast.Constant(self.flakiness_prob)),
            zero,
            epsilon
        )

        summation_expression = ast.Expression(ast.BinOp(left=ast.Name(id='summand'), op=ast.Add(), right=if_expr))

        for i in range(summation_depth-1):
            summation_expression = \
                ast.Expression(ast.BinOp(left=ast.Name(id='summand'), op=ast.Add(), right=summation_expression))

        return ast.FunctionDef(
            'flaky_summation_' + function_identifier,
            ast.arguments([], [ast.arg(arg='summand')], defaults=[]),
            [ast.Return(summation_expression)],
            []
        )

    # Generates one line function that asserts equality between the call of the flaky function and non-flaky summation
    def generate_test_tree(self, summand, summation_depth, function_identifier):
        test_function = ast.FunctionDef(
            'test_sum_' + function_identifier,
            ast.arguments([], [], defaults=[]),
            [self.generate_assert_equality_expression(
                ast.Call(func=ast.Name('random_api.flaky_summation_' + function_identifier), args=[ast.Constant(summand)], keywords=[]),
                ast.Constant(summation_depth*summand)
            )],
            []
        )
        return test_function
