from __future__ import print_function

import csv, itertools, sys
import numpy as np

from itertools import combinations, chain
import numpy as np
import csv
from run import Run
from runner import Runner
from logireg import logitReg
from numpy import std



def zeromean(column):
    #center the data at 0 mean
    avg = np.average(column)
    return column-avg

def divbystd(column):
    
    std = np.std(column)
    return column/std


def fillMissing(x):
    present=0
    sum=0
    for i in range(x.shape[0]):
        if x[i] is None or np.isnan(x[i]):
            continue
        else:
            present=present+1
            sum=sum+x[i]
    avg=float(sum)/float(present)
    for i in range(x.shape[0]):
        if x[i] is None or np.isnan(x[i]):
            x[i]=avg
        


def load_train_data():
    with open('Project1_data_training.csv', 'r') as f:
        data = list(csv.reader(f))
        del data[905]
        return map(Runner, data)
    
def powerset(iterable):
    # adapted from https://docs.python.org/2/library/itertools.html#recipes
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))

def is_2015_marathon(event):
    #classify if an event is the needed target event
    return 'Marathon Oasis' in event.name and \
       event.date.year == 2015 and \
       event.event_type == 'marathon'


def has_2015_marathon(runner):
    #classify the target variable
    if any(map(is_2015_marathon, runner.events)):
        return 1
    else:
        return 0

features_list = {
        'age': lambda r: r.age,
        'sex': lambda r: int(r.sex == 'M'),
        'event_count': lambda r: len(r.events),
        'avg_dist': lambda r: r.get_avg_dist(0),
        'run_ratio': lambda r: r.get_run_ratio(),
        'timeweight': lambda r: r.get_race_timeweight(),
        '2011': lambda r: r.ran_in_2011,
        '2012': lambda r: r.ran_in_2012,
        '2013': lambda r: r.ran_in_2013,
        '2014': lambda r: r.ran_in_2014,
        '2015': lambda r: r.ran_in_2015,
        'finishing_ratio': lambda r: r.finishing_ratio(),
}
feature = {'age','sex','event_count', 'avg_dist','run_ratio','perf','timeweight','2011','2012','2013','2014','2015','finishing_ratio'}
def features(runner, feature_list):
    features = [
            features_list[f](runner) for f in feature_list
    ]
    return features

def has_all_features(runner, flist):
    fs = features(runner, flist)
    return all(map(lambda f: f is not None, fs))

# def toValue(runner):
#     

def cross_validation(data):
    
    for i in range(data.shape[1]):
        fillMissing(data[:,i])
    data=data.astype(float)
    folds=np.array_split(data,10)
    accu=[]
    #list of accuracy
    for i in xrange(len(folds)):
        validation = folds[i]
        if i==0:
            data=np.vstack(folds[1:])
        elif (i==len(folds)-1):
            data=np.vstack(folds[:i-1])
        else:
            data=np.vstack((np.vstack(folds[:i]),np.vstack(folds[i+1:])))

        X=data[:,:data.shape[1]-1]

        Y=data[:,data.shape[1]-1]
        
        logit=logitReg(X,Y,data.shape[1]-1)
        
        tol = 1e-3
        logit.train(X, Y, tol)
        test_X=validation[:,:data.shape[1]-1]
        test_Y=validation[:,data.shape[1]-1]
        result,testY,accuracy = logit.predict(test_X, test_Y)
        accu.append(accuracy)
    return np.mean(accu),logit

def load_test_data():
    with open('Project1_data_TEST.csv', 'r') as f:
        data = list(csv.reader(f))
        return map(Runner, data)

def load_predict_data():
    with open('Project1_data.csv', 'r') as f:
        data = list(csv.reader(f))
        del data[0]
        return map(Runner, data)
    
    
if __name__ == "__main__":
    train=load_train_data()
    feature_list=features_list

    X= np.asarray([features(runner, feature_list) for runner in train])
    for i in range(X.shape[1]):
        fillMissing(X[:,i])
    X=X.astype(float)

    X[:,4]=zeromean(X[:,4])
    X[:,4]=divbystd(X[:,4])

    Y=np.asarray(map(has_2015_marathon,train))
    full_data=np.column_stack((X,Y))
    full_data=full_data.astype(float)
    accuracy,model=cross_validation(full_data)
    print ('crossvalidation')
    print (accuracy)
    test=load_test_data()
    test_X=np.asarray([features(runner, feature_list) for runner in test])
    test_X=test_X.astype(float)
    for i in range(test_X.shape[1]):
        fillMissing(test_X[:,i])
    
    test_Y=(np.asarray(map(has_2015_marathon,test)))
    test_Y=test_Y.astype(float)
    t_res,t_Y,test_acc=model.predict(test_X,test_Y)
    
    print('test')
    print(test_acc)
    
    pred=load_predict_data()
    #predicting for 2016
    pred_X=np.asarray([features(runner, feature_list) for runner in pred])
    pred_X=pred_X.astype(float)
    for i in range(pred_X.shape[1]):
        fillMissing(pred_X[:,i])
    pred_Y=np.zeros(pred_X.shape[0])
    p_res,p_Y,p_acc=model.predict(pred_X,pred_Y)
    id=np.arange(pred_X.shape[0])

    result=np.column_stack((id,p_res))
    np.savetxt('logistic_result.csv',result,fmt='%i',delimiter=',')
                    

    