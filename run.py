from __future__ import division

import re
from datetime import datetime, timedelta


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

class Run(object):

    # input: runner (a Runner object)
    #        data: kwargs containing --
    #           date, name, type, time, category
    def __init__(self, runner, **data):
        type_label = fix_type_label(data['type'])

        self.runner = runner
        self.runner_uid = runner.uid
        self.name = data['name']
        self.category = data['category']
        self.event_type = type_label
        self.date = datetime.strptime(data['date'], '%Y-%m-%d')
        self.year = self.date.year
        self.distance = self.get_distance_from_type(type_label)
        self.time = None
        self.finished = False
        if data['time'] != '-1':
            self.finished = True
            time = datetime.strptime(data['time'], '%H:%M:%S')
            self.time = self.get_time(timedelta(
                       hours=time.hour, minutes=time.minute, seconds=time.second))

        self.avg_run_speed = self.get_avg_speed_from_type(type_label)


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
    def get_time(self, time_obj):
        portion_running = 1
        if self.event_type is 'ironman':
            portion_running = 0.4

        elif self.event_type is 'half ironman':
            portion_running = 0.4

        else:
            portion_running = 1

        return timedelta(seconds=(portion_running*(time_obj.total_seconds())))
    def get_avg_speed_from_type(self, type_label):
    #TODO: are we only going to make this count for marathon distances? I think so
    # http://www.runtri.com/2011/06/how-long-does-it-take-to-finish-ironman.html
    # We can determine which portion of the time is devoted to the speed
        if self.time== None:
            return 0
        else:
            return (self.distance*1000)/(self.time.total_seconds())

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
            return -1 #need a better value than this

    def __repr__(self):
        return "<Run: {runner_uid} - {name} ({event_type})>".format(**self.__dict__)

    def __str__(self):
        return "{uid},{name},{etype},{date},{distance},{category}".format(
                uid=self.runner_uid,
                name=self.name,
                etype=self.event_type,
                date=self.date.strftime('%Y-%m-%d'),
                distance=str(self.distance) if self.distance else 'N/A',
                category=self.category)

