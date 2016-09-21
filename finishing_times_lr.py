import csv, itertools
import numpy as np

from itertools import combinations, chain

from run import Run
from runner import Runner

DATA_FILEPATH = 'data/Project1_data.csv'

def flatten(l):
    return [item for sublist in l for item in sublist]

def powerset(iterable):
    # adapted from https://docs.python.org/2/library/itertools.html#recipes
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))

def load_data():
    with open(DATA_FILEPATH, 'r') as f:
        return map(Runner, list(csv.reader(f))[1:])


def is_2015_marathon(event):
    return 'Marathon Oasis' in event.name and \
       event.date.year == 2015 and \
       event.event_type == 'marathon' and \
       event.time is not None


def has_2015_marathon(runner):
    return any(map(is_2015_marathon, runner.events))

def has_all_features(runner, flist):
    fs = features(runner, flist)
    return all(map(lambda f: f is not None, fs))

features_list = {
        'age': lambda r: r.age,
        'sex': lambda r: int(r.sex == 'M'),
        'avg_dist': lambda r: r.get_avg_dist(0),
        #'timeweight': lambda r: r.get_avg_timeweight(),
        'speed': lambda r: r.get_avg_speed(),
}

def features(runner, feature_list):
    features = [
            features_list[f](runner) for f in feature_list
    ]
    return features

def closed_form(data, l=0):
    # TODO: assert shapes
    # takes a feature matrix of the form 
    #   [ [feature_1 for datum 1, feature_2 for datum 1, ... ], ... ]
    # l is the regularization constant which defaults to zero
    Y, X = zip(*data)
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

def err(w, data):
    # data has the form [ (y, [f1, f2, ...]), ...]
    w = flatten(w.tolist())
    return sum( (y - sum(map(np.prod, zip(w, row))))**2 for y, row in data) 


def cross_validation(data):
    # take in data, return mean err on cross validation
    np.random.shuffle(data)
    fold_size = len(data) // 10
    remainder = fold_size % 10
    folds = [data[i:i+fold_size] for i in xrange(0,len(data), fold_size)]
    # add the remainders to the last fold
    folds[-1].extend(data[fold_size-remainder:])
   
    errs = []
    for i in xrange(len(folds)):
        validation = folds[i]
        data = flatten(folds[:i] + folds[i+1:])
        w = closed_form(data)
        errs.append(err(w, validation))
    
    return np.mean(errs)


if __name__ == "__main__":
    runners = filter(has_2015_marathon, load_data())
    marathon_2015_times = {}
    for runner in runners:
        marathon_2015 = next((e for e in runner.events if is_2015_marathon(e)))
        marathon_2015_times[runner.uid] = marathon_2015.time.seconds
        del runner.events[runner.events.index(marathon_2015)]

    
    errs = []    
    for feature_list in powerset(features_list):
        # filter the data on runners who have a data point for the 2015 marathon
        # as this is our Y. We also want to make sure we have data for all the 
        # featues and that the montreal marathon isn't their only event
        filtered_runners = filter(
                lambda r: has_all_features(r, feature_list), 
                runners)
        # get Y and remove it from the data
        Y = [marathon_2015_times[r.uid] for r in filtered_runners]

        # now build X 
        X = [features(runner, feature_list) for runner in filtered_runners]
    
        #split into 10 for 10-fold validation
        data = zip(Y, X)

        errs.append((feature_list, cross_validation(data)/len(data), len(data)))

    errs.sort(lambda a, b: int(a[1] - b[1]))

    import pprint

    pprint.pprint(errs)

