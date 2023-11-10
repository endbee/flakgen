import ast

from generation.random_api.random_api import RandomApiGenerator


class MultiplicationGenerator(RandomApiGenerator):

    def __init__(self, flakiness_prob):
        self.flakiness_prob = flakiness_prob

    # Generates a function that multiplies a multiplicand with itself as often as the multiplication depth indicates and
    # inverts the expression with some prob, like multiplicand=2, mulitplication_depth=3: 2 * 2 * 2 or -(2 * 2 * 2)
    def generate_flaky_function_tree(self, multiplication_depth, function_identifier):
        minus_one = ast.Constant(-1)
        one = ast.Constant(1)

        if_expr = ast.IfExp(
            self.generate_compare_lt_expression(self.generate_random_float_number_expression(),
                                                ast.Constant(self.flakiness_prob)),
            one,
            minus_one
        )

        multiplication_expression = ast.Expression(ast.BinOp(left=ast.Name(id='multiplicand'), op=ast.Mult(), right=if_expr))

        for i in range(multiplication_depth - 1):
            multiplication_expression = \
                ast.Expression(ast.BinOp(left=ast.Name(id='multiplicand'), op=ast.Mult(), right=multiplication_expression))

        return ast.FunctionDef(
            'flaky_multiplication_' + function_identifier,
            ast.arguments([], [ast.arg(arg='multiplicand')], defaults=[]),
            [ast.Return(multiplication_expression)],
            []
        )

    # Generates one line function that asserts equality between the call
    # of the flaky function and non-flaky multiplication
    def generate_test_tree(self, multiplicand, multiplication_depth, funciton_identifier):
        return ast.FunctionDef(
            'test_multiplication_' + funciton_identifier,
            ast.arguments([], [], defaults=[]),
            [self.generate_assert_equality_expression(
                ast.Call(func=ast.Name('random_api.flaky_multiplication_' + funciton_identifier), args=[ast.Constant(multiplicand)], keywords=[]),
                ast.Constant(multiplicand ** multiplication_depth)
            )],
            []
        )
