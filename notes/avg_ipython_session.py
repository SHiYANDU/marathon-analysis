import csv
from runner import Runner
from run import Run
with open('data/Project1_data.csv', 'r') as f:
    runners = map(Runner, list(csv.reader(f))[1:])
events = ['marathon', 'half marathon']
f = lambda run: run.event_type in events
for runner in runners:
    runner.events = filter(f, runner.events)
runners = filter(lambda r: len(r.events), runners)
len(runners)
%ed
import numpy as np
means = {}
std_devs = {}
%ed
from __future__ import division
def calc_avg(runner):
    speeds = [ e.distance / e.time.seconds for e in runner.events]
    means[runner.uid] = np.mean(speeds)
    std_devs[runner.uid] = np.std(speeds)
map(calc_avg, runners)
runners[0]
runners[0].events[0]
r = runners[0].events[0]
r.time
r.time.seconds
%ed calc_avg
means
%ed calc_avg
means = {}
std_Devs
std_devs
std_devs = {}
map(calc_avg, runners)
len(means)
len(std_devs)
anomolies = []
for runner in runners:
    mean = means[runner.uid]
    std = std_devs[runner.uid]
    for r in runner.events:
        if r.finished:
            speed = r.distance*1000/r.time.seconds
            if speed <= mean - 2*std or speed >= mean +2*std:
                anomolies.append(r)
len(anomolies)
from op import plus
from ops import plus
from operations import plus
from operation import plus
from operator import plus
from operator import add
reduce(add,map(lambda r: len(r.events),runners))
len(anomolies)
len(set(map(lambda e: e.name, anomolies)))
reduce(lambda a, b: a.union(b), map(lambda r: set(r.events),runners))
len(reduce(lambda a, b: a.union(b), map(lambda r: set(map(lambda e: e.name, r.events)),runners)))
len(anomolies)
len(set(map(lambda e: e.name, anomolies)))
reduce(add,map(lambda r: len(r.events),runners))
from collections import Counter
anomoly_count = Counter(map(lambda e: e.name, anomolies))
anomoly_count.most_common()
name_count = Counter([ e.name for r in runners for e in r.events])
name_count.most_common()
top_three = ["Marathon Oasis Rock \xe2\x80\x98n\xe2\x80\x99 Roll de Montr\xc3\xa9al", "Marathon Oasis de Montreal", "Marathon Oasis Rock 'n' Roll de Montreal"]
average_dates = Counter([ e.date.strftime('%Y-%m-%d') for r in runner for e in r.events if e.name in top_three])
average_dates = Counter([ e.date.strftime('%Y-%m-%d') for r in runners for e in r.events if e.name in top_three])
average_dates
average_dates = Counter([ e.name + ': ' + e.date.strftime('%Y-%m-%d') for r in runners for e in r.events if e.name in top_three])
average_dates
nonavg_dates = Counter([ e.name + ': ' + e.date.strftime('%Y-%m-%d') for e in anomolies if e.name in top_three])
nonavg_dates
top_three = ['Marathon des Deux Rives L\xc3\xa9vis-Qu\xc3\xa9bec']
nonavg_dates = Counter([ e.name + ': ' + e.date.strftime('%Y-%m-%d') for e in anomolies if e.name in top_three])
nonavg_dates
[ len(r.events) for r in runners if 'Marathon des Deux Rives L\xc3\xa9vis-Qu\xc3\xa9bec: 2012-08-26' in map(lambda e: e.name, r.events)]
[ len(r.events) for r in runners if 'Marathon des Deux Rives L\xc3\xa9vis-Qu\xc3\xa9bec' in map(lambda e: e.name, r.events)]

