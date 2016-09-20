import csv
from __future__ import division
from run import Run
from runner import Runner
d = datetime.strptime('2015-01-01', '%Y-%m-%d')
from datetime import datetime
d = datetime.strptime('2015-01-01', '%Y-%m-%d')
f = lambda r: r.date < d
with open('data/Project1_data.csv','r') as f:
    runners = map(Runner, list(csv.reader(f))[1:])
for runner in runners:
    runner.events = filter(f, runner.events)
f = lambda r: r.date < d
for runner in runners:
    runner.events = filter(f, runner.events)

events = set([e.name for r in runners for e in r.events])
events = Counter([e.name for r in runners for e in r.events])
from collections import Counter
events = Counter([e.name for r in runners for e in r.events])
events
len(events)
events.most_common()[:5]
events.most_common()[:10]
[ e for e in events if 'Oasis' in e]
[ e for e in events if 'Marathon Oasis' in e]
1/2
overlap = {}
for event in events:
    rs = filter(lambda r: event.name in map(lambda e:e.name,r.events),runners)
    overlap[event.name] = len(filter(lambda r: any(map(lambda e: 'Marathon Oasis' in e, r.events)), rs))/len(rs)
for event in events:
    rs = filter(lambda r: event in map(lambda e:e.name,r.events),runners)
    overlap[event.name] = len(filter(lambda r: any(map(lambda e: 'Marathon Oasis' in e, r.events)), rs))/len(rs)
for event in events:
    rs = filter(lambda r: event in map(lambda e:e.name,r.events),runners)
    overlap[event.name] = len(filter(lambda r: any(map(lambda e: 'Marathon Oasis' in e.name, r.events)), rs))/len(rs)
for event in events:
    rs = filter(lambda r: event in map(lambda e:e.name,r.events),runners)
    overlap[event.name] = len(filter(lambda r: any(map(lambda e: 'Marathon Oasis' in e.name, r.events)), rs))/len(rs)
events
for event in events:
    rs = filter(lambda r: event in map(lambda e:e.name,r.events),runners)
    overlap[event.name] = len(filter(lambda r: any(map(lambda e: 'Marathon Oasis' in e.name, r.events)), rs))/len(rs)
event = 'YMCA of Peterborough Half-marathon and 5km'
rs = filter(lambda r: event in map(lambda e:e.name,r.events),runners)
rs
rs[0].events
filter(lambda r: any(map(lambda e: 'Marathon Oasis' in e.name, r.events)), rs)
rs
len(filter(lambda r: any(map(lambda e: 'Marathon Oasis' in e.name, r.events)), rs))/len(rs)
common_events = events.most_common[:100]
common_events = events.most_common()[:100]
for event in commom_events:
    rs = filter(lambda r: event in map(lambda e:e.name,r.events),runners)
    overlap[event.name] = len(filter(lambda r: any(map(lambda e: 'Marathon Oasis' in e.name, r.events)), rs))/len(rs)
for event in common_events:
    rs = filter(lambda r: event in map(lambda e:e.name,r.events),runners)
    overlap[event.name] = len(filter(lambda r: any(map(lambda e: 'Marathon Oasis' in e.name, r.events)), rs))/len(rs)
for event in common_events:
    rs = filter(lambda r: event in map(lambda e:e.name,r.events),runners)
    if rs:
        overlap[event.name] = len(filter(lambda r: any(map(lambda e: 'Marathon Oasis' in e.name, r.events)), rs))/len(rs)
overlap
for event in common_events:
    rs = filter(lambda r: event in map(lambda e:e.name,r.events),runners)
    if rs:
        print rs
        overlap[event.name] = len(filter(lambda r: any(map(lambda e: 'Marathon Oasis' in e.name, r.events)), rs))/len(rs)
common_events
len(runners)
len(common_events)
for event in common_events:
    rs = filter(lambda r: event in map(lambda e:e.name,r.events),runners)
    if rs:
        print rs
        overlap[event.name] = len(filter(lambda r: any(map(lambda e: 'Marathon Oasis' in e.name, r.events)), rs))/len(rs)
e = common_events[0]
e
rs = filter(lambda r: event in map(lambda e:e.name,r.events),runners)
rs
r = runners[0]
r.events
r = runners[2].events
r
map(lambda e:e.name,r.events)
r = runners[2]
map(lambda e:e.name,r.events)
for event, count in common_events:
    rs = filter(lambda r: event in map(lambda e:e.name,r.events),runners)
    if rs:
        print rs
        overlap[event.name] = len(filter(lambda r: any(map(lambda e: 'Marathon Oasis' in e.name, r.events)), rs))/len(rs)
for event, count in common_events:
    rs = filter(lambda r: event in map(lambda e:e.name,r.events),runners)
    if rs:
        overlap[event] = len(filter(lambda r: any(map(lambda e: 'Marathon Oasis' in e.name, r.events)), rs))/len(rs)
overlap
events['Vert le Raid - XC de la Vallee']
rs = filter(lambda r: 'Vert le Raid - XC de la Vallee' in map(lambda e:e.name,r.events),runners)
rs
map(lambda r: r.events, rs)
map(lambda r: filter(lambda e: 'Oasis' in e.name or 'Vert' in e.name, r.events), rs)
map(lambda r: filter(lambda e: 'Oasis' in e.name or 'Vert le Raid - XC de la Vallee' in e.name, r.events), rs)
overlaps = map(lambda r: filter(lambda e: 'Oasis' in e.name or 'Vert le Raid - XC de la Vallee' in e.name, r.events), rs)
overlaps_dates = [ [ e.name + ': '+ e.date.strftime('%Y-%m-%d') for e in re] for re in overlaps]
overlaps_dates
for event, count in common_events:
    rs = filter(lambda r: event in map(lambda e:e.name,r.events),runners)
    if rs:
        overlap = filter(
            lambda r: filter(
                lambda e: e.name=='Marathon Oasis de Montreal' and
                          e.date > event.date and
                          e.date < event.date + timedelta(days=365), r.events
                ),
            rs)
for event, count in common_events:
    rs = filter(lambda r: event in map(lambda e:e.name,r.events),runners)
    if rs:
        overlap = set()
        for r in rs:
            for r_e in filter(lambda e: e.name == event, r.events):
                for e in filter(lambda e: e.name == 'Marathon Oasis de Montreal', r.events):
                    if e.date > r_e.date and e.date < (r_e.date + timedelta(days=265)):
                        overlaps.add(r)
     overlaps[event] = len(overlap)/len(rs)
chron_overlaps = {}
for event, count in common_events:
    rs = filter(lambda r: event in map(lambda e:e.name,r.events),runners)
    if rs:
        overlap = set()
        for r in rs:
            for r_e in filter(lambda e: e.name == event, r.events):
                for e in filter(lambda e: e.name == 'Marathon Oasis de Montreal', r.events):
                    if e.date > r_e.date and e.date < (r_e.date + timedelta(days=265)):
                        overlaps.add(r)
    chron_overlaps[event] = len(overlap)/len(rs)
from datetime import timedelta
for event, count in common_events:
    rs = filter(lambda r: event in map(lambda e:e.name,r.events),runners)
    if rs:
        overlap = set()
        for r in rs:
            for r_e in filter(lambda e: e.name == event, r.events):
                for e in filter(lambda e: e.name == 'Marathon Oasis de Montreal', r.events):
                    if e.date > r_e.date and e.date < (r_e.date + timedelta(days=265)):
                        overlaps.add(r)
    chron_overlaps[event] = len(overlap)/len(rs)
for event, count in common_events:
    rs = filter(lambda r: event in map(lambda e:e.name,r.events),runners)
    if rs:
        overlap = set()
        for r in rs:
            for r_e in filter(lambda e: e.name == event, r.events):
                for e in filter(lambda e: e.name == 'Marathon Oasis de Montreal', r.events):
                    if e.date > r_e.date and e.date < (r_e.date + timedelta(days=265)):
                        overlap.add(r)
    chron_overlaps[event] = len(overlap)/len(rs)
chron_overlaps
sorted(chron_overlaps.iteritems(), lambda a, b: a[1] - b[1])
sorted(chron_overlaps.iteritems(), lambda a, b: a[1] < b[1])
sorted(chron_overlaps.iteritems(), lambda a, b: -1 if a[1] < b[1] else 0 if a[1] == b[1] else 1)
sorted(chron_overlaps.iteritems(), lambda a, b: 1 if a[1] < b[1] else 0 if a[1] == b[1] else -1)
events['Course des iles']
rs = filter(lambda r: 'Course des iles' in map(lambda e:e.name,r.events),runners)
len(rs)
overlaps = map(lambda r: filter(lambda e: 'Oasis' in e.name or 'Course des iles' in e.name, r.events), rs)
overlaps_dates = [ [ e.name + ': '+ e.date.strftime('%Y-%m-%d') for e in re] for re in overlaps]
overlaps_dates
overlaps = map(lambda r: filter(lambda e: 'Oasis' in e.name or 'Course des iles' in e.name, r.events), rs) ;
overlaps_dates = [ [ e.name + ': '+ e.date.strftime('%Y-%m-%d') for e in re] for re in overlaps];
def get_deted_overlaps(event):
    overlaps = map(lambda r: filter(lambda e: 'Oasis' in e.name or event in e.name, r.events), rs)
    overlaps_dates = [ [ e.name + ': '+ e.date.strftime('%Y-%m-%d') for e in re] for re in overlaps]
    return overlap_dates
chron_overlaps_sorted = sorted(chron_overlaps.iteritems(), lambda a, b: 1 if a[1] < b[1] else 0 if a[1] == b[1] else -1)
chron_overlaps_sorted
chron_overlaps_sorted[:10]
get_deted_overlaps('Demi-Marathon Marcel Jobin')
%ed get_deted_overlaps
get_dated_overlaps('Demi-Marathon Marcel Jobin')
%ed get_dated_overlaps
%ed get_dated_overlaps
get_dated_overlaps('Demi-Marathon Marcel Jobin')
chron_overlaps_sorted[:10]
get_dated_overlaps('Tour du Lac Brome')
chron_overlaps_sorted[:10]
get_dated_overlaps('D\xc3\xa9fi Hivernal Ile Bizard')
chron_overlaps_sorted[:10]
get_dated_overlaps('Course du Fort de Chambly')
chron_overlaps_sorted[:10]
get_dated_overlaps('La Grande Viree des Sentiers St-Bruno')
history

