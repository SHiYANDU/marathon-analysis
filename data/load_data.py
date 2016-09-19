# script to take in the format provided by the project
# clean it up a little and load it into a usable OO format

import argparse, csv, re
from collections import Counter
from datetime import datetime, timedelta

DATA_FILEPATH = 'Project1_data.csv'

def group_events(row):
    # turn each row into a list of lists where each sublist is:
    #    ['EVENT DATE', 'EVENT NAME', 'EVENT TYPE', 'TIME', 'CATEGORY']
    return zip(*map(lambda i: row[1+i::5], range(5))) #lambda grabs the next 5 elements from the list

    #I THINK THIS IS WRONG. I DON'T THINK WE CAN MAKE THe ASSUMPTION IT IS ONLy TH ENEXT 5 ELEMENTS. Oh nvm it maps them

def load_data(outfile, write_runs, write_runners, filters={}):
    with open(DATA_FILEPATH, 'r') as f:
        data = list(csv.reader(f))[1:] #ignores the first line

    data = [Runner(row) for row in data] #make a runner object for each row in data

    if filters is not None:
        for func in filters:
            for runner in data:
                runner.events = filter(func, runner.events)

    if write_runs:
        with open(outfile + '_runs.csv', 'w+') as f:
            f.write('RUNNER,NAME,TYPE,DATE,DISTANCE,CATEGORY\n')
            for runner in data:
                for run in runner.events:
                    f.write(str(run)+'\n')
    if write_runners:
        with open(outfile + '_runners.csv', 'w+') as f:
            # TODO update once more features are added

            f.write('RUNNER,AGE,GENDER,EVENT COUNT, AVG DISTANCE, TOTAL DISTANCE, PERFORMANCE, AVG SPEED\n')
            for runner in data:
                f.write(str(runner)+'\n')

def make_date_filter(date):
    # takes date in format 'YYYY-MM-DD'
    date = datetime.strptime(date, '%Y-%m-%d')
    def f(run):
        return run.date < date

    return f

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
        'olympique': 'olympic',
         re.compile('.*70\.3.*$'):'half ironman',
        re.compile('(^\s+|\s+$)'): '',
    }
#last thing I don't understand.
#
    return reduce(
            lambda s, rule: re.sub(rule[0], rule[1], s),
            rules.iteritems(),
            label.lower())

def split_gender_and_age(category):
    rules = {
        ' ': '',
         re.compile('.*\+.*$'):'N/A', #anything plus becomes hard to bin
         re.compile('m '): 'm',
         re.compile('f '): 'f',
         'maitre': '',
         ',': '-',


    }
    cleaned = reduce(
            lambda s, rule: re.sub(rule[0], rule[1], s),
            rules.iteritems(),
            category.lower())


    if cleaned is "N/A" or cleaned is '':
        return [-1, -1]

    age = bin_age(cleaned)
    gender = get_gender(cleaned)

    return[age, gender]


def get_gender(cleaned):

    if "f" in cleaned:
        return 1

    elif "m" in cleaned:
        return 0
    else:
        return -1

def bin_age(cleaned): #take upper number
    arange = cleaned[1:].split('-')
    print(arange)
    if (len(arange) is 1) or (len(arange) is 0) or '' in arange or len(arange[0]) > 2 or len(arange[1]) >2:
        return -1

    else:
        return (int(arange[0]) + int(arange[1]))/ 2


#on the first pass, it takes the label, and runs through the lambda on it. Then it does it again. and so on

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

        #grou events creates a list of the events each runner has run in, which is a bit confusing imo. So group_events creates a list of lists of each event, and then labels each. I guess that makes sense.i Each runner has a bunch of dicts. Events is a series of run objects
        events = map(lambda event: dict(zip(labels,event)), group_events(row))

        #OPTIMIZE THIS SO ITS ALL IN ONE LOOP.
        self.events = [Run(self,**event) for event in events]
        distances = [run.distance for run in self.events]
        speeds = [run.avg_run_speed for run in self.events]
        genders = [run.gender for run in self.events]
        ages = [run.avg_age for run in self.events]
        self.total_distance = sum(distances)
        self.performance_metric = sum(map(self.performance_function, distances))
        self.num_events= len(self.events)
        self.avg_dist = self.total_distance/self.num_events
        self.avg_speed = sum(speeds)/self.num_events
        self.gender = sum(genders)/self.num_events
        self.avg_avg_age = sum(ages)/self.num_events



    def performance_function(self, element):
        return element**2

    def __repr__(self):
        return "<Runner: {uid}>".format(**self.__dict__)

    def __str__(self):
        return '{uid},{age},{gender},{event_count},{avg_distance},{tot_distance},{perf},{avg_speed}'.format(
                age=self.avg_avg_age,
                gender=self.gender,
                uid=self.uid,
                event_count=self.num_events,
                avg_distance = self.avg_dist,
                tot_distance = self.total_distance,
                perf = self.performance_metric,
                avg_speed = self.avg_speed
            )

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
        self.time = None
        self.finished = False
        self.category = split_gender_and_age(data['category'])
        self.avg_age = self.category[0]
        self.gender = self.category[1]
        #if data['time'] == '-1':
        self.finished = False
        if data['time'] != '-1':
            self.finished = True
        #else:
            time = datetime.strptime(data['time'], '%H:%M:%S')
            self.time = timedelta(
                       hours=time.hour, minutes=time.minute, seconds=time.second)

        self.avg_run_speed = self.get_avg_speed_from_type(type_label)


    def get_avg_speed_from_type(self, type_label):
    #TODO: are we only going to make this count for marathon distances? I think so
    # http://www.runtri.com/2011/06/how-long-does-it-take-to-finish-ironman.html
    # We can determine which portion of the time is devoted to the speed
        if self.time== None:
            return 0
        else:
            return (self.distance*1000)/(self.time.total_seconds())



    distance_re = re.compile('(?P<dist>\d+(\.\d+)?)km')
    run_distances = {
        "marathon": 42.195,
        "half marathon": 21.0975,
        "sprint duathlon": 7.5,
        "duathlon":  15,
        "ironman": 42.220,
        "half ironman": 21.1, #NOTE a 70.3 is  ahalf marathon# all 70.3 go to half ironman. contains half and ironman, half ironman etc
        "sprint triathlon": 5,
        "olympic triathlon": 10,
    }

    def get_distance_from_type(self, type_label):
        #TODO: update with marathon and half marathon
        self.time = 0
        match = self.distance_re.match(type_label)
        if match is not None:
            d = match.groups()[0]
            if d is not None:
                d = float(d)
            return d
        elif type_label.lower() in self.run_distances:
            return  float(self.run_distances[type_label.lower()])
        else:
            return 1

    def __repr__(self):
        return "<Run: {runner_uid} - {name} ({event_type})>".format(**self.__dict__)

    def __str__(self):
        return "{uid},{name},{avg_age},{gender},{etype},{date},{distance},{category},{avg_speed}".format(
                uid=self.runner_uid,
                name=self.name,
                avg_age=self.age,
                gender = self.gender,
                etype=self.event_type,
                date=self.date.strftime('%Y-%m-%d'),
                distance=str(self.distance) if self.distance else 'N/A',
                category=self.category,
                avg_speed = self.avg_run_speed)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                description='Processes raw data for comp 551 project 1'
            )
    parser.add_argument('outfile', type=str,
                help="The csv to write, without the file type sufix. e.g. 'clean_data'")
    parser.add_argument('-d','--date', type=str,
                default='2015-01-01',
                help="A date to cut off data as a training set YYYY-MM-DD. e.g. 2015-01-01 will not include any running data from after 2015")
    parser.add_argument('-run','--run_data', help="write run data",
            action="store_true")
    parser.add_argument('-runner','--runner_data',help="write runner data",
            action="store_true")

    args = parser.parse_args()

    date_filter = make_date_filter(args.date)

    load_data(args.outfile, args.run_data, args.runner_data, filters=[date_filter])



#TODO
#2. remove all non runs. sort of done
#4. do naive bayes
#   http://www.runtri.com/2011/06/how-long-does-it-take-to-finish-ironman.html - depends on agegroup
#add gender, age
# bin age by every 5 years. if you aged out, we can have another feature.
