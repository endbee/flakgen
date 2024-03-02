import ast
import random
import string

from generation.generator import Generator


class BasicVictimPolluterTestOrderDependentGenerator(Generator):

    def generate_test_tree(self, number_of_tests=2):
        test_positions = list(range(0, number_of_tests))
        # chose one of the tests to be the polluter
        polluted_test = random.choice(test_positions)
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
                test_statements.extend(
                    self.generate_polluter_statements(
                        global_variable_name, global_variable_name_string)
                )
            else:
                # when victim, just assert the global variable value to be the initial value
                test_postfix = 'victim'
                test_statements.extend(
                    self.generate_victim_statements(
                        global_variable_name,
                        global_variable_name_string,
                        global_variable_value
                    )
                )

            test = ast.FunctionDef(
                f'test_{i}_{test_postfix}',
                ast.arguments([], [], defaults=[]),
                test_statements,
                []
            )
            global_scope_statements.append(test)

        return ast.Module(body=global_scope_statements)

    def generate_victim_statements(self, global_variable_name, global_variable_name_string, global_variable_value):
        victim_statements = [
            ast.Expr(ast.Global(names=[global_variable_name_string])),
            self.generate_assert_equality_expression(
                global_variable_name, global_variable_value)
        ]

        return victim_statements

    def generate_polluter_statements(self, global_variable_name, global_variable_name_string):
        polluted_value = ast.Constant(random.randint(1, 999))

        victim_statements = [
            ast.Expr(ast.Global(names=[global_variable_name_string])),
            ast.Assign(targets=[global_variable_name], value=polluted_value,
                       type_ignores=[]),
            self.generate_assert_equality_expression(
                global_variable_name, polluted_value)
        ]

        return victim_statements
