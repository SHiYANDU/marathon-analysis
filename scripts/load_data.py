# script to take in the format provided by the project
# clean it up a little and load it into a usable OO format

import csv, re
from collections import Counter
from datetime import datetime, timedelta

DATA_FILEPATH = '../data/Project1_data.csv'

def group_events(row):
    # turn each row into a list of lists where each sublist is:
    #    ['EVENT DATE', 'EVENT NAME', 'EVENT TYPE', 'TIME', 'CATEGORY']
    return zip(*map(lambda i: row[1+i::5], range(5)))

def load_data():
    with open(DATA_FILEPATH, 'r') as f:
        data = list(csv.reader(f))[1:]

    return [Runner(row) for row in data]

# a quick analysis of the event types showed a few frequent
# types which were the same with different labels.
#  For example: "10KM", "10 km", "10 k"
#  to recify this, everything was converted to lower case and 
#  these examples, the following regex is used
#   s/\s?km?/km/
#
# before any fixing, there were 574 types
# adding lowercase reduced this to 512 types
# using the regex above brought it down to 469 types
# 
# A couple more rules that each conflate a couple labels:
#    s/demi/half/
#    s/-/ /
#    s/  / /
#    s/full marathon/marathon/
#    s/run//
#    s/(^\s+|\s+$)//

def fix_type_label(label):
    rules = {
        re.compile('\s?km?'): 'km',
        'demi': 'half',
        '-': ' ',
        '  ': ' ',
        'full marathon': 'marathon',
        'run': '',
        re.compile('(^\s+|\s+$)'): '',
    }

    return reduce(
            lambda s, rule: re.sub(rule[0], rule[1], s),
            rules.iteritems(),
            label.lower())

class Runner(object):

    # input: row (row from the raw data)
    # Initializes the following fields 
    #   uid: unique ID
    #   gender: TODO
    #   age: TODO maybe we can estimate age based on categories in runs?
    #   runs: A list of Run objects
    def __init__(self, row):
        self.uid = int(row[0])

        labels = ['date','name','type','time','category']

        events = map(lambda event: dict(zip(labels,event)), group_events(row))
        self.events = [Run(self,**event) for event in events]

    def __repr__(self):
        return "<Runner: {uid}>".format(**self.__dict__)

class Run(object):

    # input: runner (a Runner object)
    #        data: kwargs containing --
    #           date, name, type, time, category
    def __init__(self, runner, **data):
        type_label = fix_type_label(data['type']) 

        self.runner = runner
        self.runner_uid = runner.uid
        self.name = data['name']
        self.event_type = type_label
        self.date = datetime.strptime(data['date'], '%Y-%m-%d')
        self.distance = self.get_distance_from_type(type_label)
        self.category = data['category']
        if data['time'] == '-1':
            self.finished = False
            self.time = None
        else:
            time = datetime.strptime(data['time'], '%H:%M:%S')
            self.time = timedelta(
                       hours=time.hour, minutes=time.minute, seconds=time.second)

    distance_re = re.compile('(?P<dist>\d+(\.\d+)?)km')
    def get_distance_from_type(self, type_label):
        match = self.distance_re.match(type_label)
        if match is not None:
            d = match.groups()[0]
            if d is not None:
                d = float(d)
            return d
        else:
            return None

    def __repr__(self):
        return "<Run: {runner_uid} - {name} ({event_type})>".format(**self.__dict__)
