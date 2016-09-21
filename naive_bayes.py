"""For each known class value,

    Calculate probabilities for each attribute, conditional on the class value.

        Use the product rule to obtain a joint conditional probability for the attributes.

            Use Bayes rule to derive conditional probabilities for the class variable.

            Once this has been done for all class values, output the class with the highest probability."""

#WE ARE ONLY TRYING TO DETERMINE IF THEY RAN THE RACE OR NOT
#features: total distance, performance metric, number of events, distance

#Need a distribution. We can either try a binomial, multinomial, or gaussian, but not all make sense. bernoulli for instance, makes sense if we try to do it by year


#function to load data. probs the one for each runner

#function to get the prior

#FOR GAUSSIAN: - works well for times, speed,
#function for the mean

import argparse, csv, re
import numpy as np
import math
from collections import Counter
from datetime import datetime, timedelta

DATA_FILEPATH = 'data/t_runners.csv'

def load_data(outfile, class_type):
    with open(DATA_FILEPATH, 'r') as f:
        data = list(csv.reader(f))

    #feature_names = data[0]
    #feature_vals = data[1:]
    #feature_matrix = np.asarray[feature_vals]
    continuous = 8

    # choose which features you want

    test = np.asarray(data[1:])

    discrete_classifier(test[:,3:6])

    if class_type is "gaussian":
        return 0
    #id, discrete, discrete, discrete, continuous, continuous, continuous, continuous



#FUNCTION: make classifier takes the class and puts into both discrete and continuous and then unites them

#Make a classifier class. initialize witha training set, and then use instances with the classify function



def classify(classifier, instance):

    #run classifier on the instance. return 0 for not in, return 1 if yes


    return 0

def make_classifier(features, types):

    type_array = np.asarray(types)
    classes = np.unique(features[:,0])

    discrete_cols = type_array[type_array == 'discrete']
    discrete = discrete_classifier(np.column_stack(features[:,0],discrete_cols))

    gaussian_cols = type_array[type_array == 'continuous']
    gaussian = gaussian_classifier(np.column_stack(features[:,0],gaussian_cols))

    priors = get_priors(features[:,0])

    def classifier(instance):
        #check to see instance is valid. as in, has same size
        #get data. pass
        #get classes
            res = map(lambda c: priors[c] * discrete[c] * gaussian[c], classes)


            #return the class that got the max
            return max(res)

        #find max

    return classifier


class Classifier(object):

    def __init__(self, features, types):
        type_array = np.asarray(types)
        classes = np.unique(features[:,0])


        priors = get_priors()

        discrete_cols = type_array[type_array == 'discrete']
        discrete = discrete_classifier(np.column_stack(features[:,0],discrete_cols))

        gaussian_cols = type_array[type_array == 'continuous']
        gaussian = gaussian_classifier(np.column_stack(features[:,0],gaussian_cols))


    def classify(instance):


    #FOR EACH CLASS, grab the probabilities given that class from discrete, multiply by product of those given by gaussian

    return 0



def discrete_classifier(features):
    classes = np.unique(features[:,0])
    total_num = len(features[:,0])
    class_features = {}
    likelihoods = {}

    priors = {}
    conditionals = {}
    #for each class, i.e. y = 0, 1, we get the features where that class is 1
    for cls in classes:
        class_features[cls] = features[features[:,0] == cls]
        #get class likelihood. If discrete, just num over n. If continuous use gaussian distribution
        #p(x = 1| y=1) is just the sum of all of the features for one of these rows, divided by the total number of features for discrete.
        #for continuous use the guassian distribution
        priors[cls] = len(features)/total_num

        for col_num in range(1,np.shape(class_features[cls])[1]):
            col = (class_features[cls][:,col_num]).astype(int)
            if str(cls) in conditionals.keys():
                conditionals[str(cls)].append(len(col[col==int(cls)])/np.shape(col)[0])
            else:
                conditionals[str(cls)] = [len(col[col==int(cls)])/np.shape(col)[0]]

    #assign likelihoods to each and choose the most likely

#5 minutes discrete

    def classifier(instance):

        vals = {}
        for c in classes:
            #for each class
            class_probs = []
            for i in range(0, len(instance)):
                class_probs.append(numpy.prod(conditionals[c]))

            vals[c] = priors[c] * np.prod(class_probs)

        return vals
    #return classifier


def gaussian_classifier(features):
    classes = np.unique(features[:,0])
    total_num = len(features[:,0])
    class_features = {}
    likelihoods = {}

    priors = {}
    conditionals = {}
    #for each class, i.e. y = 0, 1, we get the features where that class is 1
    for cls in classes:
        class_features[cls] = features[features[:,0] == cls]
        priors[el] = len(features)/total_num

        params = []

        for col_num in range(1,np.shape(class_features[cls])[1]):
            col = (class_features[cls][:,col_num]).astype(float)

            mean = np.mean(col)
            variance = np.var(col)
            params.append((mean,variance))

        conditionals[cls] = params

    def classifier(instance):
    #assume each feature lines up with each
        vals = {}
        for c in classes:
            #for each class
            class_probs = []
            for i in range(0, len(instance)):
                class_probs.append(gaussian_func(conditionals[c][i][0], conditionals[c][i][1], instance[i]))


            #vals[c] = priors[c] * np.prod(class_probs)

            vals[c] = np.prod(class_probs)

        return vals

        #FIND max
        #not yet
        #return max(vals.values())

    return classifier


def gaussian_func(mean, var, val):
    return (1/math.sqrt(2*math.pi*(var)))*math.exp((-(val-mean)**2)/(2*(var)))

def discretize(continuous_vector):

    return 0

def bin(val):
    return int(round(val))

#function for std dev
#Multinomial: - works well for

#training set
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                description='Perform naive bayes classification'
            )
    parser.add_argument('outfile', type=str,
                help="The csv to write, without the file type sufix. e.g. 'clean_data'")
    parser.add_argument('-t','--type', type=str,
                default='gaussian',
                help="type of distribution you want to use")

    args = parser.parse_args()
    load_data(args.outfile, args.type)
    print ("Select which features you want")


#Explain thoughts as I do it
#Naive
