#!/usr/bin/env python
"""
Usage: python parser.py -f <filename> -s <excel_sheet_name>

Parser for KPI Sense coding assessment.
"""
import argparse
import datetime
import json
import sys

import pandas
import pytz


DATA_FILE = 'data/Demo_Assessment_Model_08.18.20.xlsx'
DEFAULT_SOURCE = 'KPI Dashboard'
DEFAULT_SUBSET = 'all'


def excel_parser(dataframe, source=DEFAULT_SOURCE):
    """
    Return formatted json from pandas dataframe.

    :param dataframe: dataframe extracted from excel file
    :type dataframe: pandas.DataFrame
    :param str source: sheet name in excel of frame
    :return formatted json
    """
    categories = dict()

    subset = DEFAULT_SUBSET
    category = None
    dates = []

    for _, row in dataframe.iterrows():
        unique_cell_types = set(map(type, row.dropna().values))

        # Skip uninformative rows
        if len(unique_cell_types) < 2:
            continue

        # Check if row is a cateogry row
        if isinstance(row[3], datetime.datetime):
            if not dates:
                dates = [
                    x.replace(tzinfo=pytz.UTC).isoformat(
                        timespec='milliseconds')
                    for x in row if isinstance(x, datetime.datetime)]

            category = row[2].rstrip()

            if not pandas.isna(row[1]):
                subset = row[1].rstrip()

            if category in categories:
                categories[category]['subsets'].append(subset)
            else:
                categories[category] = dict(
                    name=category,
                    fields=[],
                    subsets=[subset],
                    start_date=dates[0],
                    end_date=dates[-1],
                    data = dict()
                )

        # Check if row is a data field row
        if isinstance(row[3], (float, int)):
            field_name = row[2].rstrip()

            if field_name not in categories[category]['fields']:
                categories[category]['fields'].append(field_name)

            for field_date, value in zip(dates, row[3:]):
                data_fields = categories[category]['data']

                if field_date not in data_fields:
                    data_fields[field_date] = dict(
                        date=field_date,
                        values=[]
                    )

                data_fields[field_date]['values'].append(
                    dict(
                        name=field_name,
                        subset=subset,
                        value=value,
                ))

    categories = list(categories.values())
    for cat in categories:
        cat['data'] = list(cat['data'].values())

    return dict(source=source, categories=categories)


def main(argv):
    '''
    Extract pandas Dataframe from excel file and print formatted json
    from excel parser.

    :param argv: command line arguments
    :type argv: sys.argv
    '''
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', '--filename', type=str, default=DATA_FILE,
                            help=())
    arg_parser.add_argument('-s', '--source', type=str, default=DEFAULT_SOURCE,
                            help=())

    args = arg_parser.parse_args(argv[1:])
    dataframe = pandas.read_excel(args.filename, sheet_name=args.source)

    print(json.dumps(excel_parser(dataframe), indent=2))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
