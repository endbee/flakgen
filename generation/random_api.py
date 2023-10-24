import ast


def generate_flaky_summation(summation_depth, flaky_prob):
    epsilion = ast.Constant(0.1)
    zero = ast.Constant(0)

    if_expr = ast.IfExp(
        generate_compare_eq_expression(generate_random_float_number_expression(), ast.Constant(flaky_prob)),
        zero,
        epsilion
    )

    print(ast.dump(if_expr))

    summation_expression = ast.Expression(ast.BinOp(left=ast.Name(id='summand'), op=ast.Add(), right=if_expr))

    for i in range(summation_depth-1):
        summation_expression = \
            ast.Expression(ast.BinOp(left=ast.Name(id='summand'), op=ast.Add(), right=summation_expression))

    return ast.FunctionDef(
        'flaky_summation',
        ast.arguments([], [ast.arg(arg='summand')], defaults=[]),
        [ast.Import(names=[ast.alias('numpy')]), ast.Return(summation_expression)],
        []
    )


def generate_summation_test(summation_depth):
    return ast.FunctionDef(
        'test_sum',
        ast.arguments([], [], defaults=[]),
        [generate_assert_equality_expression(
            ast.Call(func=ast.Name('flaky_summation'), args=[ast.Constant(5)], keywords=[]),
            ast.Constant(summation_depth*5)
        )],
        []
    )


def generate_assert_equality_expression(left, right):
    return ast.Assert(
        ast.Expression(
            ast.BinOp(left=left, op=ast.Eq(), right=right)
        )
    )


def generate_compare_eq_expression(left, comparator):
    return ast.Compare(left=left, keywords=[], ops=[ast.Lt()], comparators=[comparator])


def generate_random_float_number_expression():
    return ast.Call(ast.Attribute(value=ast.Name(id='numpy.random'), attr='random'), args=[], keywords=[])


def generate_flaky_summation_test_and_function_pair(summation_depth, flaky_prob):
    return generate_flaky_summation(summation_depth, flaky_prob), generate_summation_test(summation_depth)
