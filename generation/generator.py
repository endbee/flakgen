import ast


class Generator:
    # Generates expression like 'left == right'
    @staticmethod
    def generate_assert_equality_expression(left, right):
        return ast.Assert(
            ast.Expression(
                ast.BinOp(left=left, op=ast.Eq(), right=right)
            )
        )

    # Generates expression like 'left < comparator'
    @staticmethod
    def generate_compare_lt_expression(left, comparator):
        return ast.Compare(left=left, keywords=[], ops=[ast.Lt()], comparators=[comparator])