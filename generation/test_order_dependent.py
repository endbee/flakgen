import ast
import random
import string

from .generator import Generator


class BasicTestOrderDependentGenerator(Generator):

    def generate_test_tree(self, identifier, number_of_tests=2):
        test_positions = list(range(0, number_of_tests))
        polluted_test = random.choice(test_positions)
        global_variable_name_string = random.choice(string.ascii_lowercase)
        global_variable_name = ast.Name(global_variable_name_string)
        global_variable_value = ast.Constant(random.randint(1, 999))

        global_scope_statements = [
            ast.Import(names=[ast.alias('pytest')]),
            ast.Expr(ast.Global(names=[global_variable_name_string])),
            ast.Assign(targets=[global_variable_name], value=global_variable_value,
                       type_ignores=[])
        ]

        for i in range(0, number_of_tests):
            test_statements = []

            if i == polluted_test:
                polluted_value = ast.Constant(random.randint(1, 999))
                test_statements.append(ast.Expr(ast.Global(names=[global_variable_name_string])))
                test_statements.append(ast.Assign(targets=[global_variable_name], value=polluted_value,
                                                  type_ignores=[]))
                test_statements.append(self.generate_assert_equality_expression(global_variable_name, polluted_value))
            else:
                test_statements.append(ast.Expr(ast.Global(names=[global_variable_name_string])))
                test_statements.append(
                  self.generate_assert_equality_expression(global_variable_name, global_variable_value))

            test = ast.FunctionDef(
                f'test_{i}',
                ast.arguments([], [], defaults=[]),
                test_statements,
                []
            )
            global_scope_statements.append(test)

        return ast.Module(body=global_scope_statements)

    def generate_test_order_annotation_statement(self, test_order):
        return ast.Expr(
            ast.Call(ast.Attribute(value=ast.Name(id='@pytest.mark'), attr='run'), args=[], keywords=[ast.keyword(
                arg='order',
                value=ast.Name(id=ast.Constant(test_order), ctx=ast.Load()))]))
