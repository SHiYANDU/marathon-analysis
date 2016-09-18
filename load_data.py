# script to take in the format provided by the project
# clean it up a little and load it into a usable OO format

from __future__ import division

import argparse, csv, os.path
from datetime import datetime, timedelta

from run import Run
from runner import Runner

DATA_DIR = 'data'
DATA_FILEPATH = 'Project1_data.csv'

def load_data(outfile, write_runs, write_runners, filters={}):
    with open(os.path.join(DATA_DIR, DATA_FILEPATH), 'r') as f:
        data = list(csv.reader(f))[1:]

    data = [Runner(row) for row in data]

    if filters is not None:
        for func in filters:
            for runner in data:
                runner.events = filter(func, runner.events)

    outfile = os.path.join(DATA_DIR, outfile)
    if write_runs:
        with open(outfile + '_runs.csv', 'w+') as f:
            f.write('RUNNER,NAME,TYPE,DATE,DISTANCE,CATEGORY\n')
            for runner in data:
                for run in runner.events:
                    f.write(str(run)+'\n')
    if write_runners:
        with open(outfile + '_runners.csv', 'w+') as f:
            # TODO update once more features are added
            f.write('RUNNER,GENDER,AGE,EVENT COUNT\n')
            for runner in data:
                # don't write runners whose data was all filtered out:
                if len(runner.events) > 0:
                    f.write(str(runner)+'\n')

def make_date_filter(date):
    # takes date in format 'YYYY-MM-DD'
    date = datetime.strptime(date, '%Y-%m-%d')
    def f(run):
        return run.date < date

    return f

def make_type_filter(types):

    def f(run):
        return run.event_type in types

    return f

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
    parser.add_argument('-t', '--types', help="which types of event to include, defaults to all types",
            nargs='+')

    args = parser.parse_args()

    date_filter = make_date_filter(args.date)
    filters = [date_filter]
    if args.types:
        filters.append(make_type_filter(args.types))

    load_data(args.outfile, args.run_data, args.runner_data, filters=filters)



