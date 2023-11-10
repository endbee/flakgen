import ast
import random
import string

from generation.generator import Generator


class BasicVictimPolluterTestOrderDependentGenerator(Generator):

    def generate_test_tree(self, number_of_tests=2):
        test_positions = list(range(0, number_of_tests))
        polluted_test = random.choice(test_positions)  # chose one of the tests to be the polluter
        global_variable_name_string = random.choice(string.ascii_lowercase)
        global_variable_name = ast.Name(global_variable_name_string)
        global_variable_value = ast.Constant(random.randint(1, 999))

        # prepare global variable
        global_scope_statements = [
            ast.Expr(ast.Global(names=[global_variable_name_string])),
            ast.Assign(targets=[global_variable_name], value=global_variable_value,
                       type_ignores=[])
        ]

        # generate tests that are polluter or victims and add them to module
        for i in range(0, number_of_tests):
            test_statements = []

            if i == polluted_test:
                # when polluter, pollute by setting new value to global variable
                test_postfix = 'polluter'
                polluted_value = ast.Constant(random.randint(1, 999))
                test_statements.append(ast.Expr(ast.Global(names=[global_variable_name_string])))
                test_statements.append(ast.Assign(targets=[global_variable_name], value=polluted_value,
                                                  type_ignores=[]))
                test_statements.append(self.generate_assert_equality_expression(global_variable_name, polluted_value))
            else:
                # when victim, just assert the global variable value to be the initial value
                test_postfix = 'victim'
                test_statements.append(ast.Expr(ast.Global(names=[global_variable_name_string])))
                test_statements.append(
                    self.generate_assert_equality_expression(global_variable_name, global_variable_value))

            test = ast.FunctionDef(
                f'test_{i}_{test_postfix}',
                ast.arguments([], [], defaults=[]),
                test_statements,
                []
            )
            global_scope_statements.append(test)

        return ast.Module(body=global_scope_statements)
