#!/usr/bin/env python
"""
Usage: pytest

Parser for KPI Sense coding assessment.
"""
import json
import parser

import pandas


DEFAULT_TEST_FILE = 'data/Demo_Assessment_Model_08.18.20.xlsx'
DEFAULT_SOURCE = 'KPI Dashboard'
EXPECTED_FILE = 'data/part_1_expected_extracted.json'


def get_parsed_excel():
    """Return parsed excel data from default sheet."""
    dataframe = pandas.read_excel(DEFAULT_TEST_FILE, sheet_name=DEFAULT_SOURCE)

    return parser.excel_parser(dataframe)


def get_data_cell_from_parsed(parsed_data, date_str, category, subset,
                              index=0):
    """Extract data schema from json by date, category, subset and index."""
    category = [x for x in parsed_data['categories']
                if x['name'] == category][0]

    values_by_date = [x for x in category['data']
                      if x['date'] == date_str][0]['values']

    return [x for x in values_by_date if
            x['subset'] == subset][index]


def test_task_one():
    """Test Task 1 against expecte json file"""
    parsed_data = get_parsed_excel()

    for category in parsed_data['categories']:
        del category['data']

    expected = json.loads(open(EXPECTED_FILE).read())

    assert json.dumps(expected) == json.dumps(parsed_data)


def test_task_two():
    """Test Task 2 against expected value from first and last data cell."""
    parsed_data = get_parsed_excel()

    expected_first_data_cell = dict(name='Subscription Revenue', subset='all',
                                    value=26258.8)
    expected_last_data_cell = dict(name='YTD Net Expansion Revenue',
                                   subset='OPM', value=-6763)

    start_date = '2018-01-31T00:00:00.000+00:00'
    end_date = '2020-12-31T00:00:00.000+00:00'
    first_category = 'Summary Financial Metrics'
    last_category = 'MRR/ARR by Month'
    first_subset, last_subset = 'all', 'OPM'


    first_data_cell_dict = get_data_cell_from_parsed(
        parsed_data, start_date, first_category, first_subset)
    last_data_cell_dict = get_data_cell_from_parsed(
        parsed_data, end_date, last_category, last_subset, index=-1)

    assert (json.dumps(expected_first_data_cell) ==
            json.dumps(first_data_cell_dict))
    assert (json.dumps(expected_last_data_cell) ==
            json.dumps(last_data_cell_dict))
