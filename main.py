import generation.random_api as random_api
import os
import astor


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
            f = open("testsuite/random_api_test.py", "w")

            for kind in flakiness_category_generators[category]:
                generator = flakiness_category_generators[category][kind]
                func_tree = generator.generate_flaky_function_tree()
                test_tree = generator.generate_test_tree()

                f.write(astor.to_source(test_tree))
                f.write("\n")
                f.write(astor.to_source(func_tree))
                f.write("\n")
        f.close()

    stream = os.popen('cd testsuite && pytest && cd ../..')
    output = stream.read()
    print(output)


if __name__ == "__main__":
    main()
