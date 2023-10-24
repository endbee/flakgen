import ast
import random


def generate_sum_function():
    print(random.randint(0,1))
    return ast.FunctionDef(
        'sum',
        ast.arguments([], [ast.arg(arg='summand1'), ast.arg(arg='summand2')], defaults=[]),
        [ast.Return(ast.Expression(ast.BinOp(left=ast.Name(id='summand1'), op=ast.Add(), right=ast.Name(id='summand2'))))],
        []
    )


def generate_sum_test():
    return ast.FunctionDef(
        'test_sum',
        ast.arguments([], [], defaults=[]),
        [ast.Assert(ast.Expression(ast.BinOp(left=ast.Call(func=ast.Name('sum'), args=[ast.Constant(5), ast.Constant(5)], keywords=[]), op=ast.Eq(), right=ast.Constant(10))))],
        []
    )


def generate_flaky_summation(summation_depth):
    epsilion = ast.Constant(0.1)
    zero = ast.Constant(0)
    if_expr = ast.IfExp(ast.Compare(left=ast.Call(ast.Attribute(value=ast.Name(id='random'), attr='randint'),
              [ast.arg(ast.Constant(0)), ast.arg(ast.Constant(1))], keywords=[]), ops=[ast.Eq()], comparators=[ast.Constant(0)]), zero, epsilion)

    expr = ast.Expression(ast.BinOp(left=ast.Name(id='summand'), op=ast.Add(), right=if_expr))

    for i in range(summation_depth-1):
        expr = ast.Expression(ast.BinOp(left=ast.Name(id='summand'), op=ast.Add(), right=expr))

    return ast.FunctionDef(
        'flaky_summation',
        ast.arguments([], [ast.arg(arg='summand')], defaults=[]),
        [ast.Import(names=[ast.alias('random')]), ast.Return(expr)],
        []
    )


def generate_summation_test(summation_depth):
    return ast.FunctionDef(
        'test_sum',
        ast.arguments([], [], defaults=[]),
        [ast.Assert(ast.Expression(
            ast.BinOp(left=ast.Call(func=ast.Name('flaky_summation'), args=[ast.Constant(5)], keywords=[]),
                      op=ast.Eq(), right=ast.Constant(summation_depth*5))))],
        []
    )


def generate_flaky_test_and_function_pair():
    return generate_flaky_summation(), generate_summation_test()