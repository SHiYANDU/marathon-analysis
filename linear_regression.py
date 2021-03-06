from __future__ import print_function

import csv, itertools, sys
import numpy as np

from datetime import timedelta
from itertools import combinations, chain
from multiprocessing import Pool

from run import Run
from runner import Runner

DATA_FILEPATH = 'Project1_data_training.csv'
TEST_SET_FILEPATH = 'TEST_DATA_DONT_TOUCH/Project1_data_TEST.csv'

def flatten(l):
    return [item for sublist in l for item in sublist]

def powerset(iterable):
    # adapted from https://docs.python.org/2/library/itertools.html#recipes
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))

def load_data():
    with open(DATA_FILEPATH, 'r') as f:
        return map(Runner, csv.reader(f))

def load_test_data():
    with open(TEST_SET_FILEPATH, 'r') as f:
        return map(Runner, csv.reader(f))
   


def is_2015_marathon(event):
    return 'Marathon Oasis' in event.name and \
       event.date.year == 2015 and \
       event.event_type == 'marathon'


def has_2015_marathon(runner):
    return any(map(is_2015_marathon, runner.events))

def has_all_features(runner, flist):
    fs = features(runner, flist)
    return all(map(lambda f: f is not None, fs))

features_list = {
        'age': lambda r: r.age,
        'sex': lambda r: int(r.sex == 'M'),
        'avg_dist': lambda r: r.get_avg_dist(0),
        'timeweight': lambda r: r.get_race_timeweight(),
        'speed': lambda r: r.get_avg_speed(),
        'speed_sqd': lambda r: r.get_avg_speed()**2,
        'one_over_speed': lambda r: 0 if r.get_avg_speed() == 0 else 1/r.get_avg_speed(),
        '5k': lambda r: r.avg_5k_speed(),
        '10k': lambda r: r.avg_10k_speed(),
        'half_mthn': lambda r: r.avg_half_marathon_speed(),
        'mthn': lambda r: r.avg_marathon_speed(),
        'finishing_ratio': lambda r: r.finishing_ratio(),
}

def features(runner, feature_list, default=None):
    features = [
            features_list[f](runner) for f in feature_list
    ]
    features = map(lambda f: [f, default][f is None], features)
    return features

def closed_form(data, l=0):
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
    return sum( (y - sum(map(np.prod, zip(w, row + [1]))))**2 for y, row in data) 


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

def test_feature_list(feature_list, subtract_means=False):
    print("Testing feature list: {}".format(', '.join(feature_list)),file=sys.stderr)
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

    if subtract_means:
        # get the mean for each column
        means = map(np.mean, zip(*X))
        
        no_mean = ['age', 'finishing_ratio', 'timeweight', 'sex']
    
        for item in no_mean:
            if item in feature_list:
                means[feature_list.index(item)] = 0
    
        X = [np.subtract(row, means).tolist() for row in X]

    #split into 10 for 10-fold validation
    data = zip(Y, X)

    return (feature_list, cross_validation(data)/len(data), len(data))

def plot_each_feature():
    import matplotlib.pyplot as plt

    for feature, f in features_list.iteritems():
        data = [(marathon_2015_times[r.uid], [f(r)]) for r in runners if f(r)] 
        try:
            w = closed_form(data).T.tolist()[0]
        except np.linalg.linalg.LinAlgError:
            print("Feature {} produces a singular matrix".format(feature))
            continue
        print(w)
        fit = lambda x: w[0]*x + w[1]
        y, x = zip(*data)
        domain = np.linspace(min(flatten(x)), max(flatten(x)), num=50)

        fig = plt.figure()
        plt.plot(x, y, '.')
        plt.plot(domain, fit(domain), '-')

        fig.suptitle('Fit: '+feature, fontsize=20)
        plt.xlabel(feature)
        plt.ylabel('2015 finishing time')
        fig.savefig('plots/{}.jpg'.format(feature))
        plt.clf()
        


def validate_feature_combos():
    p = Pool(4)
    errs = p.map(test_feature_list, powerset(features_list)) 
    errs.sort(lambda a, b: int(a[1] - b[1]))
    pprint.pprint(errs)

def eval_fit(runner, w, feature_list):
    w = flatten(w.tolist())
    x = features(runner, feature_list) + [1]

    return sum(map(np.prod, zip(w, x)))


def set_errors():
    feature_list = (
            '10k',
            'finishing_ratio', 
            'half_mthn', 
            'timeweight', 
            'age', 
            'mthn', 
    )

    data = [
            (marathon_2015_times[r.uid], features(r, feature_list)) 
            for r in runners
        ]

    w = closed_form(data)
    test_runners = filter(has_2015_marathon, load_test_data())
    test_marathon_2015_times = {}
    for runner in test_runners:
        marathon_2015 = next((e for e in runner.events if is_2015_marathon(e)))
        if marathon_2015.time:
            test_marathon_2015_times[runner.uid] = marathon_2015.time.seconds
        else:
            test_marathon_2015_times[runner.uid] = -1
        del runner.events[runner.events.index(marathon_2015)]

    test_data = [  
            (test_marathon_2015_times[r.uid], features(r, feature_list)) 
            for r in test_runners
        ]

    print("Training error: ", err(w, data), len(data))
    print("Validation error: ", err(w, test_data), len(test_data))
      

def make_predictions():
    feature_list = (
            '10k',
            'finishing_ratio', 
            'half_mthn', 
            'timeweight', 
            'age', 
            'mthn', 
    )
    data = [
            (marathon_2015_times[r.uid], features(r, feature_list)) 
            for r in runners
        ]

    # for this we'll use all the data to build our model
    test_runners = filter(has_2015_marathon, load_test_data())
    test_marathon_2015_times = {}
    for runner in test_runners:
        marathon_2015 = next((e for e in runner.events if is_2015_marathon(e)))
        if marathon_2015.time:
            test_marathon_2015_times[runner.uid] = marathon_2015.time.seconds
        else:
            test_marathon_2015_times[runner.uid] = -1
        del runner.events[runner.events.index(marathon_2015)]


    test_data = [  
            (test_marathon_2015_times[r.uid], features(r, feature_list)) 
            for r in test_runners
        ]


    w = closed_form(data + test_data)

    print(w)

    all_runners = [
            (str(r.uid), str(timedelta(seconds=int(eval_fit(r, w, feature_list)))))
            for r in load_data() + load_test_data()
    ]
    
    all_runners.sort(lambda a, b: int(a[0]) - int(b[0]))

    with open('linear_regression_predictions.csv','w+') as f:
        f.write('\n'.join(map(lambda row: ','.join(row), all_runners)))


def pca(X):
    # find the eigenvectors of the covariance matrix sorted by eigenvalue
    X = np.matrix([row + [1] for row in X]).T

    cov = X.dot(X.T) 
    
    # subtract the mean from each column
    cov -= cov.mean(0)

    evals, evecs = np.linalg.eigh(cov)

    # the evals are returned in increasing order and we want the 
    # eigenvec associated with the larged eval, so
    proj = evecs[-1]

    print(evals)

if __name__ == "__main__":
    import pprint
    runners = filter(has_2015_marathon, load_data())
    marathon_2015_times = {}
    for runner in runners:
        marathon_2015 = next((e for e in runner.events if is_2015_marathon(e)))
        if marathon_2015.time:
            marathon_2015_times[runner.uid] = marathon_2015.time.seconds
        else:
            marathon_2015_times[runner.uid] = -1
        del runner.events[runner.events.index(marathon_2015)]

    
    validate_feature_combos()

