import ast

from generation.generator import Generator


class ClassesBrittleStateSetterTestOrderDependentGenerator(Generator):

    @staticmethod
    def generate_class_definition(class_identifier, state_identifier, dummy_function_return):
        class_body = []

        state_name = f'member_state_{state_identifier}'

        class_member = ast.Assign(targets=[ast.Name(state_name)], value=ast.Constant('failure_state'))

        class_member_setter = ast.FunctionDef(
            f'set_{state_name}',
            ast.arguments([], [ast.arg('self'), ast.arg('value')], defaults=[]),
            [ast.Assign(targets=[ast.Name(f'self.{state_name}')], value=ast.alias('value'))],
            []
        )

        class_member_getter = ast.FunctionDef(
            f'get_{state_name}',
            ast.arguments([], [ast.arg('self'), ], defaults=[]),
            [ast.Return(ast.Name(f'self.{state_name}'))],
            []
        )

        class_dummy_function = ast.FunctionDef(
            f'dummy_function',
            ast.arguments([], [ast.arg('self'), ], defaults=[]),
            [ast.Return(ast.Constant(dummy_function_return))],
            []
        )

        class_body.append(class_member)
        class_body.append(class_member_setter)
        class_body.append(class_member_getter)
        class_body.append(class_dummy_function)

        class_def = ast.ClassDef(
            name=f'class_brittle_state_setter_{class_identifier}',
            bases=[],
            body=class_body,
            decorator_list=[],
        )

        return class_def

    def generate_test_tree(self, class_identifier, state_identifier, dummy_function_return):
        class_instance_name = 'instance'

        statements = self.generate_initializing_statements(class_identifier, class_instance_name)

        brittle = self.generate_brittle(state_identifier, class_instance_name)
        state_setter = self.generate_state_setter(state_identifier, class_instance_name, dummy_function_return)

        statements.append(brittle)
        statements.append(state_setter)

        return ast.Module(statements)

    def generate_brittle(self, state_identifier, class_instance_name):
        actual = ast.Name('actual')
        expected = ast.Name('expected')
        actual_value = ast.Call(func=ast.Name(f'instance.get_member_state_{state_identifier}'), args=[], keywords=[])

        brittle_statements = [
            ast.Global([class_instance_name]),
            ast.Assign(targets=[actual], value=actual_value,
                       type_ignores=[]),
            ast.Assign(targets=[expected], value=ast.Constant('success_state'),
                       type_ignores=[]),
            self.generate_assert_equality_expression(actual, expected)
        ]

        return ast.FunctionDef(
            f'test_brittle',
            ast.arguments([], [], defaults=[]),
            brittle_statements,
            []
        )

    def generate_state_setter(self, state_identifier, class_instance_name, dummy_function_return):
        state_setter_statements = [
            ast.Global([class_instance_name]),
            ast.Expr(
                ast.Call(func=ast.Name(f'instance.set_member_state_{state_identifier}'), args=[ast.Constant('success_state')],
                         keywords=[])),
            self.generate_assert_equality_expression(
                ast.Call(func=ast.Name(f'instance.some_function'), args=[], keywords=[]),
                ast.Constant(dummy_function_return)
            )
        ]

        return ast.FunctionDef(
            f'test_state_setter',
            ast.arguments([], [], defaults=[]),
            state_setter_statements,
            []
        )

    @staticmethod
    def generate_initializing_statements(class_identifier, class_instance_name):
        class_module_identifier = f'test_order_dependent_classes_brittle_state_setter_{class_identifier}_class'
        class_identifier = f'class_brittle_state_setter_{class_identifier}'
        class_instance = ast.Name(class_instance_name)

        class_instance_value = ast.Call(
            func=ast.Name(f'{class_module_identifier}.{class_identifier}'),
            args=[],
            keywords=[],
        )

        return [
            ast.Import(names=[ast.alias(class_module_identifier)]),
            ast.Global([class_instance_name]),
            ast.Assign(targets=[class_instance], value=class_instance_value,
                       type_ignores=[])
        ]
