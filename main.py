from generation.generation import generate_sum_function, generate_sum_test, generate_flaky_summation, generate_summation_test
import os
import astor

def main():

    func_string = astor.to_source(generate_flaky_summation(5))
    test_string = astor.to_source(generate_summation_test(5))

    if not os.path.exists('bin'):
        os.makedirs('bin')

    f = open("bin/test_sample1.py", "w")
    f.write(func_string)
    f.write("\n")
    f.write(test_string)
    f.close()

    stream = os.popen('cd bin && pytest && cd ..')
    output = stream.read()
    print(output)


if __name__ == "__main__":
    main()
