#!/usr/bin/env python

"""
Sage Bionetworks
Xindi Guo
March 2021
FHA Project
"""

import argparse
import csv
import os

import pandas
from pandas.api.types import is_numeric_dtype


def read_count_file(count_file):
    """Return a DataFrame
       Read the count file depending on the delimiter 
         and remove the gene column if it exists
    """
    with open(count_file, 'r') as input_file:
        dialect = csv.Sniffer().sniff(input_file.readline())
    df = pandas.read_csv(count_file, sep=dialect.delimiter)
    col2 = df.iloc[:,1]
    if not is_numeric_dtype(col2.dtype):
        df.drop(df.columns[[1]], axis=1, inplace=True)
    df.columns.values[0] = "guide_id"
    return df


def _find_ntc_family(guide_id):
    """Return a String of the NTC family
    """
    guide_id_list = guide_id.split('_')
    return '_'.join(guide_id_list[0:2])

def add_missing_ntc(count_df, ntc_df):
    """ Return a DataFrame
        Add missing NTC rows and freq according to NTC list
    """
    ntc_df['family'] = ntc_df['guide_id'].apply(lambda x: _find_ntc_family(x))
    ntc_df = ntc_df.merge(count_df, how='left', on='guide_id')
    ntc_df_group = ntc_df.groupby('family')
    ntc_df_list = []
    for name, group_df in ntc_df_group:
        colvalues_dict = {}
        for colname, colvalues in group_df.items():
            if colname not in ['guide_id','family']:
               colvalues_dict[colname] = colvalues.sum()
        group_df_new = group_df.fillna(colvalues_dict)
        ntc_df_list.append(group_df_new)
    ntc_df_final = pandas.concat(ntc_df_list)
    ntc_df_final.drop(['family'], axis=1, inplace=True)
    count_df_final = pandas.concat([count_df,ntc_df_final])
    cols_numeric = count_df_final.columns.values[1:]
    count_df_final[cols_numeric] = count_df_final[cols_numeric].apply(lambda x: pandas.to_numeric(x,downcast='integer'))
    count_df_final.drop_duplicates(inplace=True)
    return count_df_final

def main():
    parser = argparse.ArgumentParser(
        description="Add missing NTC rows according to NTC family and existing higest freq"
    )
    parser.add_argument(
        "-f", "--file", help="<Required> Count file", required=True
    )
    parser.add_argument(
        "-r", "--reference", help="<Required> Reference NTC file", required=True
    )
    parser.add_argument(
        "-o", "--output", help="<Optional> Output file name. Default: [count file name]_add_ntc.txt"
    )

    args = parser.parse_args()
    
    count_df = read_count_file(args.file)
    ntc_df = pandas.read_csv(args.reference,names=['guide_id'])
    output_df = add_missing_ntc(count_df, ntc_df)

    if(args.output):
        output_name = args.output
    else:
        output_name = os.path.splitext(os.path.basename(args.file))[0]+"_add_ntc.txt"

    output_df.to_csv(output_name, sep="\t", index=False)


if __name__ == "__main__":
    main()
