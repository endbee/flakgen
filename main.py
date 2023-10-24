from generation.random_api import generate_flaky_summation_test_and_function_pair
import os
import astor

def main():

    func_tree, test_tree = generate_flaky_summation_test_and_function_pair(5, 0.5)

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
