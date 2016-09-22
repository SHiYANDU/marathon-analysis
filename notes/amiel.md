# Looking for anomolies

Considering only marathons and half marathons now

### Looking for anomolies in races:
- Look for runs that have an average speed that is more than two std devs away from mean

When only considering 'half marathon' and 'marathon', there are 113 unique event names.

There are 14324 runs. When only taking those that are two stddevs from the runner's average, we get 5593 runs over 28 unique event names
The three most common races account for almost all the data points

The races are:
    - Marathon Oasis Rock 'n' Roll de Montreal
    - Marathon Oasis de Montreal
    - Marathon Oasis Rock \xe2\x80\x98n\xe2\x80\x99 Roll de Montr\xc3\xa9al

This doesn't tell us too much because these races also happen to the most common ones in general.

Something worth noting is that the ratio of non-average race time for "Marathon Oasis Rock 'n' Roll de Montreal" is 2861/3819, while the ratio for 'Marathon des Deux Rives L\xc3\xa9vis-Qu\xc3\xa9bec' is 4/383. Maybe the latter is a good metric for average running time?


Next, let's look at the date distribution for the three leading races contributing to the non-average run times.

Nothing interesting here. Looks like there's only one data point for all of them except Marathon Oasis de Montreal, but this one seems to have roughly the same proportion of non-average and average finishing times for both dates.


So it looks like there are a bunch of other marathons that have more average running times (i.e. less points in the anomoly list). Let's compare average speed for these races


### Intersection of races

loaded data, removed data from 2015

379 unique event names. Let's get the proportion of people who do one event also do a
oasis marathon

OK, looks like there are a bunch of events where everyone who did that event also
participated in the marathon. But this doesn't take date into consideration.

Let's not look for events, where participants were in Marathon Oasis de Montreal in the following year.

Looks like there are a bunch of 0s now, and a new higher values. Maybe this could be a feature!


The highest hitting one, 'Course des iles', only occured once in 2012.

Looking for a recurring example with a decent ratio (> 0.6):
- Tour du Lac Brome
- D\xc3\xa9fi Hivernal Ile Bizard
- La Grande Viree des Sentiers St-Bruno

#### Finding scores on the indicator races

Here is the important bits from the ipython session

```python
import csv
from __future__ import division
from run import Run
from runner import Runner
from datetime import datetime, timedelta
with open('data/Project1_data.csv','r') as f:
    runners = map(Runner, list(csv.reader(f))[1:])
from collections import Counter
events = Counter([e.name for r in runners for e in r.events])
common_events = events.most_common()[:100]
chron_overlaps = {}
for event, count in common_events:
    rs = filter(lambda r: event in map(lambda e:e.name,r.events),runners)
    if rs:
        overlap = set()
        for r in rs:
            for r_e in filter(lambda e: e.name == event, r.events):
                for e in filter(lambda e: 'Marathon Oasis' in e.name, r.events):
                    if e.date > r_e.date and e.date < (r_e.date + timedelta(days=265)):
                        overlap.add(r)
    chron_overlaps[event] = len(overlap)/len(rs)
def get_dated_overlaps(event):
    overlaps = map(lambda r: filter(lambda e: 'Oasis' in e.name or event in e.name, r.events), rs)
    overlap_dates = [ [ e.name + ': '+ e.date.strftime('%Y-%m-%d') for e in re] for re in overlaps]
    return overlap_dates
chron_overlaps_sorted = sorted(chron_overlaps.iteritems(), lambda a, b: 1 if a[1] < b[1] else 0 if a[1] == b[1] else -1)
chron_overlaps_sorted[:30]
```

The final output from above is:
```python
[('Demi-Marathon Bonneville de Lachine', 0.9),
 ('Demi-Marathon des \xc3\x89rables', 0.8814814814814815),
 ('La Grande Viree des Sentiers St-Bruno', 0.868421052631579),
 ('30 km sur les rives de Boucherville', 0.8653846153846154),
 ('Tour du Lac Brome', 0.7794117647058824),
 ('Course des iles', 0.7777777777777778),
 ('Demi-marathon Bonneville de Lachine', 0.7647058823529411),
 ('Banque Scotia 21km et 5km', 0.7643884892086331),
 ('Demi-marathon des glaces', 0.7605633802816901),
 ('Defi Gerard Cote de St-Hyacinthe', 0.75),
 ('Demi Marathon de Sherbrooke', 0.7468354430379747),
 ("Course d'ete des iles de Boucherville", 0.7241379310344828),
 ('Course de la Fondation hopital Saint Jerome', 0.723404255319149),
 ('Demi-Marathon Marcel Jobin', 0.7111111111111111),
 ('Defi Physio Extra de Terrebonne', 0.7),
 ('D\xc3\xa9fi Tri-O-Lacs', 0.675),
 ('Des Chenes Toi', 0.6666666666666666),
 ('D\xc3\xa9fi Bor\xc3\xa9al Sainte-Anne-de-Bellevue', 0.6620689655172414),
 ('Course Printaniere Oka', 0.6530612244897959),
 ('Coupe Dix30 2012', 0.6417910447761194),
 ('Around the Bay Road Races', 0.6413043478260869),
 ('Coupe Dix30', 0.6339285714285714),
 ('Demi Marathon International Oasis de Levis', 0.6326530612244898),
 ('Triathlon Trimemphre de Magog', 0.6213592233009708),
 ('Triathlon / Duathlon Mont-Tremblant', 0.6176470588235294),
 ('Descente Royale', 0.6153846153846154),
 ('Demi Marathon Hypothermique', 0.611764705882353),
 ('Bonjour Printemps', 0.6041666666666666),
 ('Ottawa Race Weekend', 0.5993227990970654),
 ('Ironman Mont-Tremblant 70.3', 0.5925925925925926)]
```

This represents the ratio of people who participated in the event that also participated
in the marathon the same year.

Things to note:
- This only includes the top 100 events by attendance (35 or more runners). This was done to remove issues where we get 100% just because there was only one person who ran a race and that person also ran the marathon
- These scores incude 2015
- There are also 22 races with a score of 0, if we want to keep track of a negative corralation. Though these 22 include the montreal marathon itself, because "in the next year" is a strict inequality

DO NOT USE THESE IN THEIR CURRENT STATE! They utilize what will become the test set.
Once we have a test set, the ipython session should be re-run to create new scores.
We should remove events from the indicator races that didn't have a race in 2015. Races in 2012 followed by marathons that year mean nothing to us now.


------------

Cross validation with different features

parallelized for speed

Test are as follows:

1. Base (has -1 for not finishing marathon in Y)
2. sex as -1, 1, not 0
3. subtract means from everything


Plot idea: bar chard of average error ratio for each feature compared to another bar
chart of the ratio of a few select combinations. 



