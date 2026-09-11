# this script takes the overlap table from gtalign and outputs files with the header [family, freq] and filename query
import pandas as pd
import csv, os

#input_table = '/home/jodh/scripts/small_scripts/gtalign_overlap_50_50_with_family_clean.csv'
#out_file_path = '/home/jodh/scripts/small_scripts/family_freq_tables'

input_table = sys.argv[1]
out_file_path = sys.argv[2]

def csv_to_df(input_table):
    df = pd.read_csv(input_table)
    return df

def count_family(df, duf):
    filtered_df = df[df['DUF'] == duf]
    counts = filtered_df['family'].value_counts()
    return counts

def write_file(input_table, out_file_path):
    # convert csv to pandas df
    df = csv_to_df(input_table)
    # get all unique queries in df
    dufs = df['DUF'].unique()
    for duf in dufs:
        counts = count_family(df, duf)
        out_file = os.path.join(out_file_path,duf)
        counts.to_csv(out_file, index=True)

    

if __name__ == '__main__':
    write_file(input_table, out_file_path)

