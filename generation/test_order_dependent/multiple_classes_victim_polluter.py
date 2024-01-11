import ast
import random

from generation.generator import Generator


class MultipleClassesVictimPolluterTestOrderDependentGenerator(Generator):
    @staticmethod
    def generate_class_definitions(class_state_identifiers_map):
        class_definitions = []

        for class_identifier in class_state_identifiers_map:
            class_body = []

            state_identifier = class_state_identifiers_map[class_identifier]

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
            class_definitions.append(class_def)

        return ast.Module(class_definitions)

    def generate_test_tree(
            self,
            module_identifier,
            class_state_identifiers_map,
            number_of_tests=2
    ):
        test_positions = list(range(0, number_of_tests))
        polluted_test = random.choice(test_positions)

        statements = self.generate_initializing_statements(
            module_identifier,
            class_state_identifiers_map,
        )

        for i in range(0, number_of_tests):
            test_statements = []

            if i == polluted_test:
                # when polluter, pollute by setting new value to global variable
                test_postfix = 'polluter'
                polluter_statements = self.generate_polluter_statements(class_state_identifiers_map)

                test_statements.extend(polluter_statements)

            else:
                # when victim, just assert the global variable value to be the initial value
                test_postfix = 'victim'
                victim_statements = self.generate_victim_statements(class_state_identifiers_map)

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
            class_state_identifiers_map
    ):
        victim_statements = []
        global_statements = []
        assert_statements = []

        success_state_value = ast.Constant('success_state')

        for class_identifier in class_state_identifiers_map:
            class_name = f'class_victim_polluter_{class_identifier}'
            state_identifier = class_state_identifiers_map[class_identifier]
            global_statements.append(ast.Expr(ast.Global(names=[class_name])))
            assert_statements.append(self.generate_assert_equality_expression(
                ast.Call(func=ast.Name(f'{class_name}.get_member_state_{state_identifier}'), args=[],
                         keywords=[]), success_state_value))

        random.shuffle(global_statements)
        random.shuffle(assert_statements)

        victim_statements.extend(global_statements)
        victim_statements.extend(assert_statements)

        return victim_statements

    def generate_polluter_statements(self, class_state_identifiers_map):
        polluter_statements = []
        global_statements = []
        initializing_statements = []
        assert_statements = []

        polluted_value = ast.Constant('failure_state')
        for class_identifier in class_state_identifiers_map:
            class_name = f'class_victim_polluter_{class_identifier}'
            state_identifier = class_state_identifiers_map[class_identifier]
            global_statements.append(ast.Expr(ast.Global(names=[class_name])))
            initializing_statements.append(ast.Expr(
                ast.Call(func=ast.Name(f'{class_name}.set_member_state_{state_identifier}'),
                         args=[ast.Constant('failure_state')],
                         keywords=[])))
            assert_statements.append(self.generate_assert_equality_expression(
                ast.Call(func=ast.Name(f'{class_name}.get_member_state_{state_identifier}'), args=[],
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
            class_state_identifiers_map
    ):
        class_module_identifier = f'test_order_dependent_multiple_classes_victim_polluter_{module_identifier}_class'

        initializing_statements = [ast.Import(names=[ast.alias(class_module_identifier)])]

        for class_identifier in class_state_identifiers_map:
            class_name = f'class_victim_polluter_{class_identifier}'
            class_instance = ast.Name(class_name)

            class_instance_value = ast.Call(
                func=ast.Name(f'{class_module_identifier}.{class_name}'),
                args=[],
                keywords=[],
            )
            initializing_statements.append(ast.Global([class_name]))
            initializing_statements.append(ast.Assign(targets=[class_instance], value=class_instance_value,type_ignores=[]))

        return initializing_statements

