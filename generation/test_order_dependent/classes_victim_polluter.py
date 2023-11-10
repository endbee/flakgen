import ast
import random

from generation.generator import Generator


class  ClassesVictimPolluterTestOrderDependentGenerator(Generator):
    @staticmethod
    def generate_class_definition(class_identifier, state_identifier):
        class_body = []

        state_name = f'member_state_{state_identifier}'

        class_member = ast.Assign(targets=[ast.Name(state_name)], value=ast.Constant('success_state'))

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

        class_body.append(class_member)
        class_body.append(class_member_setter)
        class_body.append(class_member_getter)

        class_def = ast.ClassDef(
            name=f'class_victim_polluter_{class_identifier}',
            bases=[],
            body=class_body,
            decorator_list=[],
        )

        return class_def

    def generate_test_tree(self, state_identifier, class_identifier, number_of_tests=2):
        class_instance_name = 'instance'
        test_positions = list(range(0, number_of_tests))
        polluted_test = random.choice(test_positions)

        statements, class_instance = self.generate_initializing_statements(class_identifier, class_instance_name)

        for i in range(0, number_of_tests):
            test_statements = []
            success_state_value = ast.Constant('success_state')

            if i == polluted_test:
                # when polluter, pollute by setting new value to global variable
                test_postfix = 'polluter'
                polluted_value = ast.Constant('failure_state')
                test_statements.append(ast.Expr(ast.Global(names=[class_instance_name])))
                test_statements.append(ast.Expr(ast.Call(func=ast.Name(f'{class_instance_name}.set_member_state_{state_identifier}'), args=[ast.Constant('failure_state')],
                         keywords=[])))
                test_statements.append(self.generate_assert_equality_expression(ast.Call(func=ast.Name(f'{class_instance_name}.get_member_state_{state_identifier}'), args=[],
                         keywords=[]), polluted_value))
            else:
                # when victim, just assert the global variable value to be the initial value
                test_postfix = 'victim'
                test_statements.append(ast.Expr(ast.Global(names=[class_instance_name])))
                test_statements.append(
                    self.generate_assert_equality_expression(ast.Call(func=ast.Name(f'{class_instance_name}.get_member_state_{state_identifier}'), args=[],
                         keywords=[]), success_state_value))

            test = ast.FunctionDef(
                f'test_{i}_{test_postfix}',
                ast.arguments([], [], defaults=[]),
                test_statements,
                []
            )

            statements.append(test)

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
                ast.Call(func=ast.Name(f'instance.set_member_state_{state_identifier}'),
                         args=[ast.Constant('success_state')],
                         keywords=[])),
            self.generate_assert_equality_expression(
                ast.Call(func=ast.Name(f'instance.dummy_function'), args=[], keywords=[]),
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
        class_module_identifier = f'test_order_dependent_classes_victim_polluter_{class_identifier}_class'
        class_identifier = f'class_victim_polluter_{class_identifier}'
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
        ], class_instance

