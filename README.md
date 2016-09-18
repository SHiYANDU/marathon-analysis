# Project 1

### Feature Ideas
Features can be implemented independently as methods on the `Run` and `Runner`.

For participation:
- Experience metric (Brendan)
- Age: An estimate based on category and event date (Amiel)
- Penalize sailing, mud runs (Brendan)
- Average distance run
- If they usually finished but didn't finish last years (Amiel)
- Number of races of any kind. People who do more races seem to be more likely to compete in this one
- sequence of races

For finishing time:
- Trend of finishing times 
- average speed (for runs only) (Brendan)
- average distance 
- age


### Things to investigate

- Do people who run Ottawa also run Montreal
- Look for anomolies, investigate potential new features (Amiel) (weather, on grass etc)
- check if sex makes a difference

### Timeline

Over the weekend

- Amiel to update load data script to remove any date range you give it
- Amiel to add filtering on load that removes non-running events


### Notes

Cross validation doesn't make sense because of the chronology of the data.


### Using the load data script

The script takes a required 'outfile' parameter which is the prefix all output
csvs will have. optional arguments are as follows

* `-d` or `--date`: The date after which to not include data (to make a testing set). Format is yyyy-mm-dd. Default is 2015-01-01.
* `-run` or `--run_data`: if this flag is present, event data is written
* `-runner` or `--runner_data`: if this flag is present, runner data is written
* `-t` or `--types`: specify the types of events you want to write. For example `-t marathon 'half marathon'` will write a CSV only with data from marathons and half marathons. If this flag is absent, then data from all types is written.


