from __future__ import division

import re
from datetime import datetime, timedelta

from run import Run

def group_events(row):
    # turn each row into a list of lists where each sublist is:
    #    ['EVENT DATE', 'EVENT NAME', 'EVENT TYPE', 'TIME', 'CATEGORY']
    return zip(*map(lambda i: row[1+i::5], range(5)))


class Runner(object):
    # category matching handles two cases:
    #    something of the form M20-24
    #    something of the form M 70+
    # Does not handle: FEMALE, M-JUN, NO AGE, ATHENA
    # At a first glance, none of the other categories have age information
    category_re = \
        re.compile('(?P<gender>[MF])\s?-?((?P<lower>\d{2})-(?P<higher>\d{2})|(?P<bound>\d{2})(?P<pm>[+-]))')

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
        # NOTE: Any methods here use ALL data, the filtering hasn't happened yet
        # I've left this here becuase I think it's pretty harmless to use test set
        # in order to get a better estimate of age and get gender info.

        # In general it's better to calculate any values as they're needed as that
        # will ensure that the test set isn't included in the feature calculation
        self.age = self.get_age()
        self.sex = self.get_sex()


    def __repr__(self):
        return "<Runner: {uid}>".format(**self.__dict__)

    def __str__(self):
        return '{uid},{sex},{age},{event_count},{avg_dist},{run_ratio},{time_weight}'.format(
                uid=self.uid,
                sex=self.sex,
                age=self.age,
                event_count=len(self.events),
                avg_dist=self.get_avg_dist(),
                run_ratio=self.get_run_ratio(),
                time_weight=self.get_race_timeweight()
            )

    # attempts to estimate the age of the runner based on categories 
    # returns the estimated age the runner will have on the day of the race
    def get_age(self):
        race_date = datetime(year=2016, month=9, day=25)
        min_age = 0
        max_age = float('inf')
        for event in self.events:
            years_ago = (race_date - event.date).days // 365
            category = self.category_re.match(event.category)
            if not category:
                continue
            category = category.groupdict()
            if category['lower'] and category['higher']:
                min_age = max(min_age, int(category['lower']) + years_ago)
                max_age = min(max_age, int(category['higher']) + years_ago)
            else:
                bound = int(category['bound'])
                if category['pm'] == '+':
                    min_age = max(min_age, bound + years_ago)
                else:
                    max_age = min(max_age, bound + years_ago)

        if min_age == 0 or max_age == float('inf'):  # we didn't find any usable data
            return None
        else:
            return (min_age + max_age) // 2

    def get_sex(self):
        sexs = map(lambda x: x[0], [e.category for e in self.events if e.category])
        # make sure we're not picking up a 'N' from NO AGE, or something
        sex = reduce(lambda c, n: n if n in ['M','H','F'] else c, sexs, None)
        return 'M' if sex == 'H' else sex
    
    # added this optional ret parameter, becuase sometime I want 0 to be the 
    # return value
    def get_avg_dist(self, ret=None):
#         get average distance of all running 
        sum=0.0
        non_run_event=0.0
        for event in self.events:
            if isinstance(event.distance,float):
                sum+=event.distance
            else:
                non_run_event+=1
        if sum==0:
            return ret
        else:
            return sum/(len(self.events)-non_run_event)
            
    def get_run_ratio(self):
#         return the proportion of running events 
        non_run_event=0.0
        for event in self.events:
            if not isinstance(event.distance,float):
                non_run_event+=1
        return (len(self.events)-non_run_event)/len(self.events)
    
    def get_race_timeweight(self):
        #average time distance of races
        time_to_evaluate=2015.0
        timeweight=0.0
        error=0.0
        for event in self.events:
            if isinstance(event.date.year,int):
                timeweight+=(time_to_evaluate-event.date.year)
            else:
                error+=1
        return timeweight/(len(self.events)-error)
    
    def get_avg_speed(self):
        dist = 0
        time = 0
        for e in self.events:
            if e.finished and e.distance:
                dist += e.distance
                time += e.finished
        if dist == 0 and time == 0:
            return 0
        else:
            return dist / time


