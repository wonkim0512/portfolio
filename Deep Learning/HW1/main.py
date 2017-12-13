# Feel free to add any functions, import statements, and variables.
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import *


def preprocessing(file):
    df = pd.read_csv(file)
    df = df.drop(['V28', 'V27', 'V26', 'V25', 'V24', 'V23', 'V22', 'V20', 'V15', 'V13', 'V8'], axis=1)
    df['scaledAmount'] = (df['Amount'] - df['Amount'].mean()) / df['Amount'].std()
    scaled_df = df.copy()
    preprocessed_df = scaled_df.drop(['Time', 'Amount'], axis=1)
    return preprocessed_df


def predict(file):
    # Fill in this function. This function should return a list of length 10,000
    #   which is filled with values in {0, 1}. For example, the current
    #   implementation predicts all the instances in test.csv as abnormal, so
    #   the precision is 0.01 and recall is 1.

    # training
    preprocessed_df = preprocessing("train.csv")
    X_train, y_train = preprocessed_df.drop("Class", axis=1), preprocessed_df.Class
    sm = SMOTE(random_state=0)
    X_train_res, y_train_res = sm.fit_sample(X_train, y_train)
    clf_rf = RandomForestClassifier(n_estimators= 100,random_state=0)
    clf_rf.fit(X_train_res, y_train_res)

    # predict
    preprocessed_test_df = preprocessing(file)
    predict = clf_rf.predict(preprocessed_test_df)
    return predict


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
