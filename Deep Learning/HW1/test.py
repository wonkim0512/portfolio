# Feel free to add any functions, import statements, and variables.


def predict(file):
    # Fill in this function. This function should return a list of length 10,000
    #   which is filled with values in {0, 1}. For example, the current
    #   implementation predicts all the instances in test.csv as abnormal, so
    #   the precision is 0.01 and recall is 1.
    return list([1 for _ in range(10000)])


def write_result(classes):
    # You don't need to modify this function.
    with open('result.csv', 'w') as f:
        f.write('Index,Class\n')
        for idx, l in enumerate(classes):
            f.write('{0},{1}\n'.format(idx, l))


def main():
    # You don't need to modify this function.
    classes = predict('test.csv')
    write_result(classes)


if __name__ == '__main__':
    # You don't need to modify this part.
    main()
