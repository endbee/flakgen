import ast
import random

from .generator import Generator


class RandomApiGenerator(Generator):

    @staticmethod
    def generate_random_float_number_expression():
        return ast.Call(ast.Attribute(value=ast.Name(id='numpy.random'), attr='random'), args=[], keywords=[])


class SummationGenerator(RandomApiGenerator):
    def __init__(self, summation_depth, flakiness_prob):
        self.summation_depth = summation_depth
        self.flakiness_prob = flakiness_prob

    def generate_flaky_function_tree(self):
        epsilon = ast.Constant(0.1)
        zero = ast.Constant(0)

        if_expr = ast.IfExp(
            self.generate_compare_eq_expression(self.generate_random_float_number_expression(), ast.Constant(self.flakiness_prob)),
            zero,
            epsilon
        )

        summation_expression = ast.Expression(ast.BinOp(left=ast.Name(id='summand'), op=ast.Add(), right=if_expr))

        for i in range(self.summation_depth-1):
            summation_expression = \
                ast.Expression(ast.BinOp(left=ast.Name(id='summand'), op=ast.Add(), right=summation_expression))

        return ast.FunctionDef(
            'flaky_summation',
            ast.arguments([], [ast.arg(arg='summand')], defaults=[]),
            [ast.Import(names=[ast.alias('numpy')]), ast.Return(summation_expression)],
            []
        )

    def generate_test_tree(self, summand):
        return ast.FunctionDef(
            'test_sum',
            ast.arguments([], [], defaults=[]),
            [self.generate_assert_equality_expression(
                ast.Call(func=ast.Name('random_api.flaky_summation'), args=[ast.Constant(summand)], keywords=[]),
                ast.Constant(self.summation_depth*summand)
            )],
            []
        )


class MultiplicationGenerator(RandomApiGenerator):

    def __init__(self, multiplication_depth, flakiness_prob):
        self.multiplication_depth = multiplication_depth
        self.flakiness_prob = flakiness_prob

    def generate_flaky_function_tree(self):
        minus_one = ast.Constant(-1)
        one = ast.Constant(1)

        if_expr = ast.IfExp(
            self.generate_compare_eq_expression(self.generate_random_float_number_expression(),
                                                ast.Constant(self.flakiness_prob)),
            one,
            minus_one
        )

        multiplication_expression = ast.Expression(ast.BinOp(left=ast.Name(id='multiplicand'), op=ast.Mult(), right=if_expr))

        for i in range(self.multiplication_depth - 1):
            multiplication_expression = \
                ast.Expression(ast.BinOp(left=ast.Name(id='multiplicand'), op=ast.Mult(), right=multiplication_expression))

        return ast.FunctionDef(
            'flaky_multiplication',
            ast.arguments([], [ast.arg(arg='multiplicand')], defaults=[]),
            [ast.Import(names=[ast.alias('numpy')]), ast.Return(multiplication_expression)],
            []
        )

    def generate_test_tree(self):
        return ast.FunctionDef(
            'test_multiplication',
            ast.arguments([], [], defaults=[]),
            [self.generate_assert_equality_expression(
                ast.Call(func=ast.Name('random_api.flaky_multiplication'), args=[ast.Constant(5)], keywords=[]),
                ast.Constant(self.multiplication_depth ** 5)
            )],
            []
        )


class ArithmeticalGenerator(RandomApiGenerator):
    OPERATORS = [ast.Add(), ast.Mult(), ast.Div(), ast.Sub()]

    def __init__(self, expression_count, flakiness_prob):
        self.expression_count = expression_count
        self.flakiness_prob = flakiness_prob
        self.arithmetical_expression = self.generate_arithmetical_expression()

    def get_random_binary_operator(self):
        return random.choice(self.OPERATORS)

    @staticmethod
    def get_random_operand():
        return ast.Constant(random.randint(1,9))

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

    def make_arithmetical_expression_flaky(self, arithmetical_expression):
        epsilon = ast.Constant(0.1)
        zero = ast.Constant(0)

        if_expr = ast.IfExp(
            self.generate_compare_eq_expression(
                self.generate_random_float_number_expression(),
                ast.Constant(self.flakiness_prob)
            ),
            zero,
            epsilon
        )

        return ast.Expression(ast.BinOp(left=arithmetical_expression, op=ast.Add(), right=if_expr))

    def generate_flaky_function_tree(self):
        return ast.FunctionDef(
            'flaky_arithmetical',
            ast.arguments([], [], defaults=[]),
            [
                ast.Import(names=[ast.alias('numpy')]),
                ast.Return(self.make_arithmetical_expression_flaky(self.arithmetical_expression))
            ],
            []
        )

    def generate_test_tree(self):
        return ast.FunctionDef(
            'test_arithmetical',
            ast.arguments([], [], defaults=[]),
            [self.generate_assert_equality_expression(
                ast.Call(func=ast.Name('random_api.flaky_arithmetical'), args=[ast.Constant(5)], keywords=[]),
                self.arithmetical_expression
            )],
            []
        )