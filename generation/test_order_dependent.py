import ast
import random
import string

from .generator import Generator


class BasicVictimPolluterTestOrderDependentGenerator(Generator):

    def generate_test_tree(self, number_of_tests=2):
        test_positions = list(range(0, number_of_tests))
        polluted_test = random.choice(test_positions)
        global_variable_name_string = random.choice(string.ascii_lowercase)
        global_variable_name = ast.Name(global_variable_name_string)
        global_variable_value = ast.Constant(random.randint(1, 999))

        global_scope_statements = [
            ast.Expr(ast.Global(names=[global_variable_name_string])),
            ast.Assign(targets=[global_variable_name], value=global_variable_value,
                       type_ignores=[])
        ]

        for i in range(0, number_of_tests):
            test_statements = []

            if i == polluted_test:
                test_postfix = 'polluter'
                polluted_value = ast.Constant(random.randint(1, 999))
                test_statements.append(ast.Expr(ast.Global(names=[global_variable_name_string])))
                test_statements.append(ast.Assign(targets=[global_variable_name], value=polluted_value,
                                                  type_ignores=[]))
                test_statements.append(self.generate_assert_equality_expression(global_variable_name, polluted_value))
            else:
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


class BasicBrittleStateSetterTestOrderDependentGenerator(Generator):

    def generate_test_tree(self, states_to_be_set=2):
        global_state_name = 'state'
        global_state = ast.Name(global_state_name)
        global_state_keys = []
        global_state_values = []

        for i in range(states_to_be_set):
            global_state_keys.append(ast.Constant(f'state_for_brittle_{i}'))
            global_state_values.append(ast.Constant('failure_state'))
            global_state_keys.append(ast.Constant(f'standalone_state_{i}'))
            global_state_values.append(ast.Constant('value'))

        global_scope_statements = [
            ast.Expr(ast.Global(names=[global_state_name])),
            ast.Assign(targets=[global_state], value=ast.Dict(keys=global_state_keys, values=global_state_values),
                       type_ignores=[])
        ]

        for i in range(states_to_be_set):
            state_setter_statements = [
                ast.Expr(ast.Global(names=[global_state_name])),
                ast.Assign(targets=[ast.Subscript(ast.Name('state'), slice=ast.Constant(f'state_for_brittle_{i}'))],
                           value=ast.Constant('success_state')),
                self.generate_assert_equality_expression(
                    ast.Subscript(ast.Name('state'), slice=ast.Constant(f'standalone_state_{i}')),
                    ast.Constant('value')
                )

            ]

            state_setter = ast.FunctionDef(
                f'test_state_setter_{i}',
                ast.arguments([], [], defaults=[]),
                state_setter_statements,
                []
            )

            global_scope_statements.append(state_setter)

            brittle_statements = [
                ast.Expr(ast.Global(names=[global_state_name])),
                self.generate_assert_equality_expression(
                    ast.Subscript(ast.Name('state'), slice=ast.Constant(f'state_for_brittle_{i}')),
                    ast.Constant('success_state')
                )
            ]

            brittle = ast.FunctionDef(
                f'test_brittle_{i}',
                ast.arguments([], [], defaults=[]),
                brittle_statements,
                []
            )

            global_scope_statements.append(brittle)

        return ast.Module(body=global_scope_statements)


class ClassesBrittleStateSetterTestOrderDependentGenerator(Generator):

    def generate_class_definition(self, identifier, state_name, dummy_function_return):

        class_body = []

        class_member = ast.Assign(targets=[ast.Name(f'member_state_{state_name}')], value=ast.Constant('failure_state'))

        class_member_setter = ast.FunctionDef(
                f'set_member_state_{state_name}',
                ast.arguments([], [ast.arg('self'), ast.arg('value')], defaults=[]),
                [ast.Assign(targets=[ast.Name(f'self.member_state_{state_name}')], value=ast.alias('value'))],
                []
            )

        class_member_getter =ast.FunctionDef(
                f'get_member_state_{state_name}',
                ast.arguments([], [ast.arg('self'),], defaults=[]),
                [ast.Return(ast.Name(f'self.member_state_{state_name}'))],
                []
            )

        class_dummy_function = ast.FunctionDef(
                f'some_function',
                ast.arguments([], [ast.arg('self'),], defaults=[]),
                [ast.Return(ast.Constant(dummy_function_return))],
                []
            )

        class_body.append(class_member)
        class_body.append(class_member_setter)
        class_body.append(class_member_getter)
        class_body.append(class_dummy_function)

        class_def = ast.ClassDef(
            name=f'class_brittle_state_setter_{identifier}',
            bases=[],
            body=class_body,
            decorator_list=[],
        )

        return class_def

    def generate_test_tree(self, identifier, state_name, dummy_function_return):
        class_instance_variable_name_string = 'instance'
        class_instance_variable_name = ast.Name(class_instance_variable_name_string)

        class_instance_value = ast.Call(
            func=ast.Name(f'test_order_dependent_classes_brittle_state_setter_{identifier}_class.class_brittle_state_setter_{identifier}'),
            args=[],
            keywords=[],
        )

        global_scope_statements = [
            ast.Import(names=[ast.alias(f'test_order_dependent_classes_brittle_state_setter_{identifier}_class')]),
            ast.Global([class_instance_variable_name_string]),
            ast.Assign(targets=[class_instance_variable_name], value=class_instance_value,
                       type_ignores=[])
        ]

        actual = ast.Name('actual')
        expected = ast.Name('expected')
        actual_value = ast.Call(func=ast.Name(f'instance.get_member_state_{state_name}'), args=[], keywords=[])

        brittle_statements = [
            ast.Global([class_instance_variable_name_string]),
            ast.Assign(targets=[actual], value=actual_value,
                       type_ignores=[]),
            ast.Assign(targets=[expected], value=ast.Constant('success_state'),
                       type_ignores=[]),
            self.generate_assert_equality_expression(actual, expected)
        ]

        brittle = ast.FunctionDef(
            f'test_brittle',
            ast.arguments([], [], defaults=[]),
            brittle_statements,
            []
        )

        state_setter_statements = [
            ast.Global([class_instance_variable_name_string]),
            ast.Expr(ast.Call(func=ast.Name(f'instance.set_member_state_{state_name}'), args=[ast.Constant('success_state')], keywords=[])),
            self.generate_assert_equality_expression(
                ast.Call(func=ast.Name(f'instance.some_function'), args=[], keywords=[]),
                ast.Constant(dummy_function_return)
            )
        ]

        state_setter = ast.FunctionDef(
            f'test_state_setter',
            ast.arguments([], [], defaults=[]),
            state_setter_statements,
            []
        )

        global_scope_statements.append(brittle)
        global_scope_statements.append(state_setter)


        return ast.Module(global_scope_statements)
