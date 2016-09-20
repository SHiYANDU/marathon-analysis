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

