import ast
from generation.generator import Generator


class TaskRaceCondGenerator(Generator):

    def generate_imports(self):
        return [
            ast.Import(names=[ast.alias('asyncio')]),
            ast.Import(names=[ast.alias('pytest')]),
            ast.Import(names=[ast.alias('random')]),
        ]

    def generate_state_init(self, init_state):
        actual = ast.Name('state')

        return ast.Assign(
            targets=[actual],
            value=ast.Constant(init_state),
            type_ignores=[]
        )

    def generate_delay_init(self):
        statements = [
            ast.Assign(
                targets=[ast.Name('delays')],
                value=ast.List([ast.Constant(1), ast.Constant(2)]),
                type_ignores=[]
            ),
            ast.Assign(
                targets=[ast.Name('success_delay')],
                value=ast.Call(ast.Name('random.choice'),
                               [ast.Name('delays')], []),
                type_ignores=[]
            ),
            ast.Expr(ast.Call(ast.Name('delays.remove'),
                     [ast.Name('success_delay')], [])),
            ast.Assign(
                targets=[ast.Name('failure_delay')],
                value=ast.Call(ast.Name('random.choice'),
                               [ast.Name('delays')], []),
                type_ignores=[]
            ),
        ]

        return statements

    def generate_success_state_setter_func(self, success_state, function_identifier):
        statements = [
            ast.Expr(ast.Await(ast.Call(ast.Name('asyncio.sleep'),
                     [ast.Name('success_delay')], []))),
            ast.Global(['state'])
        ]

        state = ast.Name('state')

        state_assignment_stmt = ast.Assign(
            targets=[state],
            value=ast.Constant(success_state),
            type_ignores=[]
        )

        statements.append(state_assignment_stmt)

        return ast.AsyncFunctionDef(
            'flaky_task_race_cond_set_success_state_' + function_identifier,
            ast.arguments([], [], defaults=[]),
            statements,
            []
        )

    def generate_failure_state_setter_func(self, failure_state, function_identifier):
        statements = [
            ast.Expr(ast.Await(ast.Call(ast.Name('asyncio.sleep'),
                     [ast.Name('failure_delay')], []))),
            ast.Global(['state'])
        ]

        state = ast.Name('state')

        state_assignment_stmt = ast.Assign(
            targets=[state],
            value=ast.Constant(failure_state),
            type_ignores=[]
        )

        statements.append(state_assignment_stmt)

        return ast.AsyncFunctionDef(
            'flaky_task_race_cond_set_failure_state_' + function_identifier,
            ast.arguments([], [], defaults=[]),
            statements,
            []
        )

    def generate_test_tree(
            self,
            function_identifier,
            success_state,
    ):
        statements = [
            ast.Global(['state']),
            ast.Assign(
                targets=[ast.Name('task1')],
                value=ast.Call(
                    ast.Name('asyncio.create_task'),
                    [ast.Call(ast.Name(
                        'flaky_task_race_cond_set_failure_state_' + function_identifier), [], [])],
                    []
                ),
                type_ignores=[]
            ),
            ast.Assign(
                targets=[ast.Name('task2')],
                value=ast.Call(
                    ast.Name('asyncio.create_task'),
                    [ast.Call(ast.Name(
                        'flaky_task_race_cond_set_success_state_' + function_identifier), [], [])],
                    []
                ),
                type_ignores=[]
            ),
            ast.Expr(ast.Await(ast.Name('task1'))),
            ast.Expr(ast.Await(ast.Name('task2'))),
            self.generate_assert_equality_expression(
                ast.Name('state'), ast.Constant(success_state))
        ]

        return ast.AsyncFunctionDef(
            'test_flaky_task_race_cond_' + function_identifier,
            ast.arguments([], [], defaults=[]),
            statements,
            [ast.Name('pytest.mark.asyncio')]
        )
