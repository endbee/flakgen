import ast
import random

from generation.generator import Generator


class MultipleClassesVictimPolluterTestOrderDependentGenerator(Generator):
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

    def generate_test_tree(
            self,
            module_identifier,
            state_a_identifier,
            class_a_identifier,
            state_b_identifier,
            class_b_identifier,
            number_of_tests=2
    ):
        class_instance_a_name = 'instance_a'
        class_instance_b_name = 'instance_b'

        test_positions = list(range(0, number_of_tests))
        polluted_test = random.choice(test_positions)

        statements, class_a_instance, class_b_instance = self.generate_initializing_statements(
            module_identifier,
            class_a_identifier,
            class_instance_a_name,
            class_b_identifier,
            class_instance_b_name
        )

        for i in range(0, number_of_tests):
            test_statements = []

            if i == polluted_test:
                # when polluter, pollute by setting new value to global variable
                test_postfix = 'polluter'
                polluter_statements = self.generate_polluter_statements(
                    class_instance_a_name,
                    class_instance_b_name,
                    state_a_identifier,
                    state_b_identifier
                )

                test_statements.extend(polluter_statements)

            else:
                # when victim, just assert the global variable value to be the initial value
                test_postfix = 'victim'
                victim_statements = self.generate_victim_statements(
                    class_instance_a_name,
                    class_instance_b_name,
                    state_a_identifier,
                    state_b_identifier,
                )

                test_statements.extend(victim_statements)

            test = ast.FunctionDef(
                f'test_{i}_{test_postfix}',
                ast.arguments([], [], defaults=[]),
                test_statements,
                []
            )

            statements.append(test)

        return ast.Module(statements)

    def generate_victim_statements(
            self,
            class_instance_a_name,
            class_instance_b_name,
            state_a_identifier,
            state_b_identifier,
    ):
        victim_statements = []
        global_statements = []
        assert_statements = []

        success_state_value = ast.Constant('success_state')

        global_statements.append(ast.Expr(ast.Global(names=[class_instance_a_name])))
        global_statements.append(ast.Expr(ast.Global(names=[class_instance_b_name])))

        assert_statements.append(
            self.generate_assert_equality_expression(
                ast.Call(func=ast.Name(f'{class_instance_a_name}.get_member_state_{state_a_identifier}'), args=[],
                         keywords=[]), success_state_value))
        assert_statements.append(
            self.generate_assert_equality_expression(
                ast.Call(func=ast.Name(f'{class_instance_b_name}.get_member_state_{state_b_identifier}'), args=[],
                         keywords=[]), success_state_value))

        random.shuffle(global_statements)
        random.shuffle(assert_statements)

        victim_statements.extend(global_statements)
        victim_statements.extend(assert_statements)

        return victim_statements

    def generate_polluter_statements(
            self,
            class_instance_a_name,
            class_instance_b_name,
            state_a_identifier,
            state_b_identifier
    ):
        polluter_statements = []
        global_statements = []
        initializing_statements = []
        assert_statements = []

        polluted_value = ast.Constant('failure_state')

        global_statements.append(ast.Expr(ast.Global(names=[class_instance_a_name])))
        global_statements.append(ast.Expr(ast.Global(names=[class_instance_b_name])))

        initializing_statements.append(ast.Expr(
            ast.Call(func=ast.Name(f'{class_instance_a_name}.set_member_state_{state_a_identifier}'),
                     args=[ast.Constant('failure_state')],
                     keywords=[])))
        initializing_statements.append(ast.Expr(
            ast.Call(func=ast.Name(f'{class_instance_b_name}.set_member_state_{state_b_identifier}'),
                     args=[ast.Constant('failure_state')],
                     keywords=[])))

        assert_statements.append(self.generate_assert_equality_expression(
            ast.Call(func=ast.Name(f'{class_instance_a_name}.get_member_state_{state_a_identifier}'), args=[],
                     keywords=[]), polluted_value))
        assert_statements.append(self.generate_assert_equality_expression(
            ast.Call(func=ast.Name(f'{class_instance_b_name}.get_member_state_{state_b_identifier}'), args=[],
                     keywords=[]), polluted_value))

        random.shuffle(global_statements)
        random.shuffle(initializing_statements)
        random.shuffle(assert_statements)

        polluter_statements.extend(global_statements)
        polluter_statements.extend(initializing_statements)
        polluter_statements.extend(assert_statements)

        return polluter_statements

    @staticmethod
    def generate_initializing_statements(
            module_identifier,
            class_a_identifier,
            class_instance_a_name,
            class_b_identifier,
            class_instance_b_name
    ):
        class_module_identifier = f'test_order_dependent_multiple_classes_victim_polluter_{module_identifier}_class'
        class_a_identifier = f'class_victim_polluter_{class_a_identifier}'
        class_a_instance = ast.Name(class_instance_a_name)
        class_b_identifier = f'class_victim_polluter_{class_b_identifier}'
        class_b_instance = ast.Name(class_instance_b_name)

        class_a_instance_value = ast.Call(
            func=ast.Name(f'{class_module_identifier}.{class_a_identifier}'),
            args=[],
            keywords=[],
        )

        class_b_instance_value = ast.Call(
            func=ast.Name(f'{class_module_identifier}.{class_b_identifier}'),
            args=[],
            keywords=[],
        )

        return [
            ast.Import(names=[ast.alias(class_module_identifier)]),
            ast.Global([class_instance_a_name]),
            ast.Global([class_instance_b_name]),
            ast.Assign(targets=[class_a_instance], value=class_a_instance_value,
                       type_ignores=[]),
            ast.Assign(targets=[class_b_instance], value=class_b_instance_value,
                       type_ignores=[])
        ], class_a_instance, class_b_instance

