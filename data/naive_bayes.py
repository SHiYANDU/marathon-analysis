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
from collections import Counter
from datetime import datetime, timedelta

DATA_FILEPATH = 'test_runners.csv'

def load_data(outfile, class_type):
    with open(DATA_FILEPATH, 'r') as f:
        data = list(csv.reader(f))

    feature_names = data[0]
    feature_vals = data[1:]

    if class_type is "gaussian":

    #RUNNER,AGE,GENDER,EVENT COUNT, AVG DISTANCE, TOTAL DISTANCE, PERFORMANCE, AVG SPEED
    #id, discrete, discrete, discrete, continuous, continuous, continuous, continuous


def gaussian_classification():

    return 0

class Gaussian(object):

    def __init__(self, data):
        self.vector = map(float(data))
        self.sample_mean = sample_mean()
        self.sample_variance = sample_variance()

    def sample_mean(self):
        return sum(self.vector)/len(self.vector)

    def sample_variance(self):
        return sum(map(lambda x: (x- self.sample_mean)**2, self.vector))/(len(self.vector) -1)

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



