import ast
import random

from generation.random_api.random_api import RandomApiGenerator


class ArithmeticalGenerator(RandomApiGenerator):
    OPERATORS = [ast.Add(), ast.Mult(), ast.Div(), ast.Sub()]

    def __init__(self, expression_count, flakiness_prob):
        self.arithmetical_expression = None
        self.expression_count = expression_count
        self.flakiness_prob = flakiness_prob

    # Generates function that calculates some flaky arithmetical expression
    def generate_flaky_function_tree(self, function_identifier):
        # Safe the non-flaky expression to have comparison base
        self.arithmetical_expression = self.generate_arithmetical_expression()

        return ast.FunctionDef(
            'flaky_arithmetical_' + function_identifier,
            ast.arguments([], [], defaults=[]),
            [
                ast.Return(self.make_arithmetical_expression_flaky(self.arithmetical_expression))
            ],
            []
        )

    # Generates one line test case that asserts equality between flaky and non-flaky arithmetical expression
    def generate_test_tree(self, function_identifier):
        return ast.FunctionDef(
            'test_arithmetical_' + function_identifier,
            ast.arguments([], [], defaults=[]),
            [self.generate_assert_equality_expression(
                ast.Call(func=ast.Name('random_api.flaky_arithmetical_' + function_identifier), args=[], keywords=[]),
                self.arithmetical_expression
            )],
            []
        )

    def get_random_binary_operator(self):
        return random.choice(self.OPERATORS)

    @staticmethod
    def get_random_operand():
        return ast.Constant(random.randint(1,9))

    # Generates expression where random numbers are concatinated with random airthmetical operators as often as the
    # expression_count indicates like, expression_count=4: 3 - 2 - 4 * 5
    def generate_arithmetical_expression(self):
        arithmetical_expression = ast.Expression(
                    ast.BinOp(
                        left=self.get_random_operand(),
                        op=self.get_random_binary_operator(),
                        right=self.get_random_operand()
                    ))

        for i in range(self.expression_count - 1):
            arithmetical_expression = \
                ast.Expression(
                    ast.BinOp(
                        left=self.get_random_operand(),
                        op=self.get_random_binary_operator(),
                        right=arithmetical_expression
                    ))

        return arithmetical_expression

    # Adds noise to an arithmetical expression with some prob
    def make_arithmetical_expression_flaky(self, arithmetical_expression):
        epsilon = ast.Constant(0.1)
        zero = ast.Constant(0)

        if_expr = ast.IfExp(
            self.generate_compare_lt_expression(
                self.generate_random_float_number_expression(),
                ast.Constant(self.flakiness_prob)
            ),
            zero,
            epsilon
        )

        return ast.Expression(ast.BinOp(left=arithmetical_expression, op=ast.Add(), right=if_expr))
