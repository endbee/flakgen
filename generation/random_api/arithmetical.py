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
        self.arithmetical_expression, statements = self.generate_arithmetical_expression()

        statements.append(ast.Return(self.make_arithmetical_expression_flaky()))

        return ast.FunctionDef(
            'flaky_arithmetical_' + function_identifier,
            ast.arguments([], [], defaults=[]),
            statements,
            []
        )

    # Generates one line test case that asserts equality between flaky and non-flaky arithmetical expression
    def generate_test_tree(self, function_identifier):
        actual = ast.Name('actual')
        expected = ast.Name('expected')
        actual_value = ast.Call(func=ast.Name('random_api.flaky_arithmetical_' + function_identifier), args=[], keywords=[])

        return ast.FunctionDef(
            'test_arithmetical_' + function_identifier,
            ast.arguments([], [], defaults=[]),
            [
                ast.Assign(targets=[actual], value=actual_value,
                           type_ignores=[]),
                ast.Assign(targets=[expected], value=self.arithmetical_expression,
                           type_ignores=[]),
                self.generate_assert_equality_expression(actual, expected)
            ],
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
        statements = []
        result = ast.Name('result')

        arithmetical_expression = ast.Expression(
                    ast.BinOp(
                        left=self.get_random_operand(),
                        op=self.get_random_binary_operator(),
                        right=self.get_random_operand()
                    ))

        assignment = ast.Assign([result], arithmetical_expression)
        statements.append(assignment)

        for i in range(self.expression_count - 1):
            operand = self.get_random_operand()
            operator = self.get_random_binary_operator()
            arithmetical_expression = \
                ast.Expression(
                    ast.BinOp(
                        left=operand,
                        op=operator,
                        right=arithmetical_expression
                    ))
            intermediate_expression = \
                ast.Expression(
                    ast.BinOp(
                        left=operand,
                        op=operator,
                        right=result
                    ))
            assignment = ast.Assign([result], intermediate_expression)
            statements.append(assignment)

        return arithmetical_expression, statements

    # Adds noise to an arithmetical expression with some prob
    def make_arithmetical_expression_flaky(self):
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

        return ast.Expression(ast.BinOp(left=ast.Name('result'), op=ast.Add(), right=if_expr))
