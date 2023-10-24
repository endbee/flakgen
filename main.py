from generation.random_api import generate_randapi_flaky_summation_test_and_function_pair
import os
import astor

def main():
    flakiness_rel = 0.5
    summation_depth = 5

    flakiness_category_generators = {
        'randapi_summation': generate_randapi_flaky_summation_test_and_function_pair
    }

    for key in flakiness_category_generators:
        if key == 'randapi_summation':
            func_tree, test_tree = flakiness_category_generators[key](summation_depth, flakiness_rel)

        if not os.path.exists('bin'):
            os.makedirs('bin')

        f = open("bin/test_sample1.py", "w")
        f.write(astor.to_source(func_tree))
        f.write("\n")
        f.write(astor.to_source(test_tree))
        f.close()

    stream = os.popen('cd bin && pytest && cd ..')
    output = stream.read()
    print(output)


if __name__ == "__main__":
    main()
