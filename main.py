import os
import astor

import generation.random_api as random_api
from file_writing.test_file_writer import TestFileWriter
from file_writing.function_file_writer import FunctionFileWriter

def main():
    flakiness_prob = 0.5
    summation_depth = 5
    multiplication_depth = 5

    flakiness_category_generators = {
        'random_api': {
            'summation': random_api.SummationGenerator(summation_depth, flakiness_prob),
            'multiplication': random_api.MultiplicationGenerator(multiplication_depth, flakiness_prob)
        }
    }

    if not os.path.exists('testsuite'):
        os.makedirs('testsuite')

    for category in flakiness_category_generators:
        if category == 'random_api':
            test_file_writer = TestFileWriter(category)
            function_file_writer = FunctionFileWriter(category)

            for kind in flakiness_category_generators[category]:
                generator = flakiness_category_generators[category][kind]
                func_tree = generator.generate_flaky_function_tree()
                test_tree = generator.generate_test_tree()

                test_file_writer.write_function(astor.to_source(test_tree))
                function_file_writer.write_function(astor.to_source(func_tree))

            test_file_writer.close()
            function_file_writer.close()

    stream = os.popen('pytest testsuite')
    output = stream.read()
    print(output)


if __name__ == "__main__":
    main()
