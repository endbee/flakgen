import ast

from .generator import Generator


class BasicTestOrderDependentGenerator(Generator):

    def generate_test_tree(self, identifier):
        return ast.Module(body=[self.generate_test_order_annotation_statement(1), self.generate_test_order_annotation_statement(2)])

    def generate_test_order_annotation_statement(self, test_order):
        return ast.Expr(ast.Call(ast.Attribute(value=ast.Name(id='@pytest.mark'), attr='run'), args=[], keywords=[ast.keyword(
            arg='order',
            value=ast.Name(id=ast.Constant(test_order), ctx=ast.Load()))]))