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

    return data


#FUNCTION: make classifier takes the class and puts into both discrete and continuous and then unites them

#Make a classifier class. initialize witha training set, and then use instances with the classify function

def make_classifier(features, types):

    type_array = np.asarray(types)
    classes = np.unique(features[:,0])

    discrete_cols = features[type_array == 'discrete']
    discrete = discrete_classifier(np.column_stack(features[:,0],discrete_cols))

    gaussian_cols = features[type_array == 'continuous']
    gaussian = gaussian_classifier(np.column_stack(features[:,0],gaussian_cols))

    priors = get_priors(features[:,0])

    def classifier(instance):
        #check to see instance is valid. as in, has same size
        #get data. pass

        #split instance into continuous and discrete
        if len(instance) != numpy.shape(features)[1] - 1:
            print( "INSTANCE NOT RIGHT SIZE. ")
            print(str(len(instance))+ " is instance size")
            print(str(numpy.shape(features)[1] - 1)+ " is instance size")
        #WHERE DO I USE THE INSTANCE?
        g = gaussian(instance[type_array == 'continuous'])
        d = discrete(instance[type_array =='discrete'])

        #get classes
        res = map(lambda c: priors[c] * d[c] * gaussian[c], classes)
        #return the class that got the max
        return classes[numpy.argmax(res)]

        #find max

    return classifier


class Classifier(object):

    def __init__(self, features, types):
        self.a = 0

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
    for cls in classes:
        class_features[cls] = features[features[:,0] == cls]

        priors[cls] = float(len(class_features[cls]))/total_num
        conditionals[cls] = []

        #conditional[Y] = [array corresponding to columns]
                                #each element in the array is a dict[class] = p(class| y)
                                #ie the probability of that class and the feature

        for col_num in range(1,np.shape(class_features[cls])[1]):

            col = (class_features[cls][:,col_num]).astype(int)
        #    if str(cls) in conditionals.keys():
            conditional_col = {}
            for opt_class in np.unique(col):
                conditional_col[opt_class] = float(len(col[col==int(opt_class)]))/np.shape(col)[0]
                #print(cls)
                #print(col_num)
                #print(float(len(col[col==int(cls)])))

            conditionals[str(cls)].append(conditional_col)

        #    else:
        #        conditionals[str(cls)] = [float(len(col[col==int(cls)]))/np.shape(col)[0]]


    def classifier(instance):

        vals = {}
        for c in classes:
            vals[c] = []
            #for each class
            class_probs = []
            print(conditionals)
            for i in range(0, len(instance)):
                #class_probs.append(np.prod(conditionals[c]))
                #class_probs.append(conditionals[c])

                vals[c].append(conditionals[(c)][i][int(instance[i])])


            vals[c] = np.prod(vals[c])
            #vals[c] = priors[c] * np.prod(class_probs)
            print("CLASS: " + c)
            #print(class_probs)
            #vals[c] = np.prod(class_probs)
            print(vals[c])

        return vals

    print(type(classifier))

    return classifier

def gaussian_classifier(features):
    classes = np.unique(features[:,0])
    total_num = len(features[:,0])
    class_features = {}
    likelihoods = {}

    priors = {}
    conditionals = {}
    for cls in classes:
        cls = int(cls)
        class_features[cls] = features[features[:,0] == cls]

        priors[cls] = float(len(class_features[cls]))/total_num
        conditionals[cls] = []

        #conditional[Y] = [array corresponding to columns]
                                #each element in the array is a dict[class] = p(class| y)
                                #ie the probability of that class and the feature

        for col_num in range(1,np.shape(class_features[cls])[1]):

            col = (class_features[cls][:,col_num]).astype(float)
        #    if str(cls) in conditionals.keys():
            conditional_col = {}
            params = (float(np.mean(col)), float(np.var(col, ddof=1)))
            print(conditionals)

            conditionals[(cls)].append(params)

    def classifier(instance):

        vals = {}
        for c in classes:
            vals[c] = []
            #for each class
            class_probs = []
            print(conditionals)
            for i in range(0, len(instance)):
                #class_probs.append(np.prod(conditionals[c]))
                #class_probs.append(conditionals[c])

                vals[c].append(gaussian_func(conditionals[c][i][0], conditionals[c][i][1] ,(float(instance[i]))))

            vals[c] = np.prod(vals[c])
            #vals[c] = priors[c] * np.prod(class_probs)
            #print("CLASS: " + c)
            #print(class_probs)
            #vals[c] = np.prod(class_probs)
            print(vals[c])

        return vals
    print(type(classifier))
    return classifier




def gaussian_func(mean, var, val):
    print(val)
    print(mean)
    print(var)
    return (float(1)/math.sqrt(2*math.pi*(var)))*math.exp((-(val-mean)**2)/(2*(var)))

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
