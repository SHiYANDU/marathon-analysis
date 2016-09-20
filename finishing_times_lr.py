import numpy as np


def closed_form(X,Y, l=0):
    # TODO: assert shapes
    # takes a feature matrix of the form 
    #   [ [feature_1 for datum 1, feature_2 for datum 1, ... ], ... ]
    # l is the regularization constant which defaults to zero
    N = len(X)

    # Add a bias term for a y-intercept then
    # take the transpose to ensure a column matrix
    X = np.matrix( [x + [1] for x in X])
    X_T = X.transpose()
    # covariance matrix
    cov = X_T.dot(X)
    Y = np.matrix(Y).transpose()

    # regularization matrix
    reg = np.matrix(l * np.identity(len(cov)))

    return np.linalg.inv(cov + reg).dot(X_T.dot(Y))


