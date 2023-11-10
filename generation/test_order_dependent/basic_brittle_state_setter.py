import ast

from generation.generator import Generator


class BasicBrittleStateSetterTestOrderDependentGenerator(Generator):

    def generate_test_tree(self, states_to_be_set=2):
        global_state_name = 'state'
        global_state = ast.Name(global_state_name)
        global_state_keys = []
        global_state_values = []

        # prepare state variable
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
            state_setter = self.generate_state_setter(global_state_name, i)
            global_scope_statements.append(state_setter)

            brittle = self.generate_brittle(global_state_name, i)
            global_scope_statements.append(brittle)

        return ast.Module(body=global_scope_statements)

    def generate_brittle(self, global_state_name, brittle_number):
        # assert state is in success state
        brittle_statements = [
            ast.Expr(ast.Global(names=[global_state_name])),
            self.generate_assert_equality_expression(
                ast.Subscript(ast.Name('state'), slice=ast.Constant(f'state_for_brittle_{brittle_number}')),
                ast.Constant('success_state')
            )
        ]
        brittle = ast.FunctionDef(
            f'test_brittle_{brittle_number}',
            ast.arguments([], [], defaults=[]),
            brittle_statements,
            []
        )
        return brittle

    def generate_state_setter(self, global_state_name, state_number):
        # set state to success state and assert standalone state
        state_setter_statements = [
            ast.Expr(ast.Global(names=[global_state_name])),
            ast.Assign(targets=[ast.Subscript(ast.Name('state'), slice=ast.Constant(f'state_for_brittle_{state_number}'))],
                       value=ast.Constant('success_state')),
            self.generate_assert_equality_expression(
                ast.Subscript(ast.Name('state'), slice=ast.Constant(f'standalone_state_{state_number}')),
                ast.Constant('value')
            )

        ]
        state_setter = ast.FunctionDef(
            f'test_state_setter_{state_number}',
            ast.arguments([], [], defaults=[]),
            state_setter_statements,
            []
        )
        return state_setter
