import ast


def generate_sum_function():
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