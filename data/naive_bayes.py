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
from collections import Counter
from datetime import datetime, timedelta

DATA_FILEPATH = 'test_runners.csv'

def load_data(outfile, class_type):
    with open(DATA_FILEPATH, 'r') as f:
        data = list(csv.reader(f))

    feature_names = data[0]
    feature_vals = data[1:]
    feature_matrix = np.asarray[feature_vals]
    continuous = 8


    if class_type is "gaussian":

    #RUNNER,AGE,GENDER,EVENT COUNT, AVG DISTANCE, TOTAL DISTANCE, PERFORMANCE, AVG SPEED
    #id, discrete, discrete, discrete, continuous, continuous, continuous, continuous


def gaussian_classification(row, feature_to_predict):
    # for every single, calculate teh prob they run in 2016
    #Then, the probability distribution of v {\displaystyle v} v given a class c {\displaystyle c} c, p ( x = v | c ) {\displaystyle p(x=v|c)} p(x=v|c), can be computed by plugging v {\displaystyle v} v into the equation for a Normal distribution parameterized by μ c {\displaystyle \mu _{c}} \mu _{c} and σ c 2 {\displaystyle \sigma _{c}^{2}} \sigma^2_c. T


    return 1 #if they will

#DO BERNOULLI

#Binned continuous for Bernoulli

def bin(val):
    return int(round(val))


class Gaussian(object):

    def __init__(self, data):
        self.vector = map(float, data)
	#CAN WE USE NUMPY?
        self.sample_mean = np.var(self.vector) #sample_mean()
        self.sample_variance = np.var(self.vector) #sample_variance()



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


#Explain thoughts as I do it
#Naive
