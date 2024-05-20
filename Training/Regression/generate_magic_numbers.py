import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
import csv

def get_values(measurement_id):
    file = open(f"./PixelToCmMapping/{measurement_id}.csv", 'r')
    reader = csv.DictReader(file)
    X_values = []
    Y_values = []
    for row in reader:
        X_values.append(float(row['Keypoint Pixel Distance']))
        Y_values.append(float(row['CM Distance']))

    return X_values,Y_values

def get_regression_result(X_values,Y_values, isDebug = False):
    # Split tto train & test dataset
    X_train = np.array([X_values[:-1200]]).reshape(-1, 1)
    X_test = np.array([X_values[-1200:]]).reshape(-1, 1)

    Y_train = np.array([Y_values[:-1200]]).reshape(-1, 1)
    Y_test = np.array([Y_values[-1200:]]).reshape(-1, 1)

    regr = linear_model.LinearRegression()
    regr.fit(X_train, Y_train)

    Y_pred = regr.predict(X_test)

    if isDebug:
        print("Coefficients: \n", regr.coef_)
        print("intercept: \n", regr.intercept_)

        print("Mean squared error: %.2f" % mean_squared_error(Y_test, Y_pred))
        print("R2: %.2f" % r2_score(Y_test, Y_pred))

        plt.scatter(X_test, Y_test, color="black")
        plt.plot(X_test, Y_pred, color="blue", linewidth=3)

        plt.xticks(())
        plt.yticks(())

        plt.show()

    return regr.intercept_[0], regr.coef_[0][0]


if __name__ == '__main__':
    measurement_mapping  = ["shoulder-breadth","chest","waist","hip"]
    with open("../../.env", "w") as f:
        for curr_id in measurement_mapping:
            X,Y = get_values(curr_id)
            intercept, coef = get_regression_result(X,Y, False)
            
            # write to .env file to use it in the whole project
            f.write(f"{curr_id.upper()}-INTERCEPT={intercept}\n")
            f.write(f"{curr_id.upper()}-COEF={coef}\n")