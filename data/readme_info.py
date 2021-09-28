#!/usr/bin/env python

# utility script to generate readme information based on CSV and datapackage
#
# pip install pandas
# usage:
#   python readme_info.py datapackage

import yaml
import sys

import pandas as pd


def readme_info(df, dp_resource):
    print('1. Number of fields: %d\n' % len(df.columns))
    print('2. Number of rows: {:,}\n'.format(len(df)))
    schema_fields = dp_resource['schema']['fields']

    assert len(schema_fields) == len(df.columns), [col for col in df.columns if not any([col == field['name'] for field in schema_fields])]
    field_info = {field['name']: field for field in schema_fields}

    print('3. Field List:')
    for col in df.columns:
        print('%s : %s' % (col, field_info[col].get('description', '')))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide path to frictionless datapackage file')
        exit(0)

    with open(sys.argv[1]) as packageyaml:
        datapackage = yaml.safe_load(packageyaml)

    for resource_dict in datapackage['resources']:
        csvfile = resource_dict['path']
        print('Inspecting %s...\n\n' % csvfile)

        df = pd.read_csv(csvfile)
        readme_info(df, resource_dict)
