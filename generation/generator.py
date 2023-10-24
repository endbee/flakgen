import ast


class Generator:
    @staticmethod
    def generate_assert_equality_expression(left, right):
        return ast.Assert(
            ast.Expression(
                ast.BinOp(left=left, op=ast.Eq(), right=right)
            )
        )

    @staticmethod
    def generate_compare_eq_expression(left, comparator):
        return ast.Compare(left=left, keywords=[], ops=[ast.Lt()], comparators=[comparator])