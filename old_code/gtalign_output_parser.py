# GTALIGN with all columns
import sys
import csv
import os
import itertools
import pandas as pd
from tabulate import tabulate

gtalign_directory_path = sys.argv[1]
num_lines = int(sys.argv[2])

gtalignDict = {}

gtalign_table = pd.DataFrame(columns=['Query_description', 'Reference_description', 'Reference_length-normalized_TM-score', 'Query_length-normalized_TM-score', 'RMSD', '#Aligned_residues', 'Query_alignment_boundaries','Reference_alignment_boundaries','Reference_length'])

for filename in os.listdir(gtalign_directory_path):
  filepath = os.path.join(gtalign_directory_path, filename)
  key = "".join(filename.split('-')[1])
  print(key)
  value = []
  temp = []
  # lines in the file that correspond to the table
  # add code to find the last_line by parsing through the file
  last_line = 0
  with open(filepath, mode='r') as gtalignfile:
    count = 0
    for i, row in enumerate(gtalignfile):
      if i > 30:
        if len(row) < 2:
          last_line = min(31+count, num_lines)
          break
        count = count+1
#  print(last_line) 
  first_line = 31
  
  with open(filepath, mode='r') as gtalignfile:
    for row in itertools.islice(gtalignfile, first_line, last_line):
      temp.append(row.split('...')[1].split('-')[0])
      temp.extend(row.split('...')[1].split()[3:])
      # value.append(row.split('...')[1].split('-')[0])
      # value.extend(row.split('...')[1].split()[3:])
      value.append(temp)
      temp = []
  gtalignDict[key] = value
# convert to pandas table
  temp_table = pd.DataFrame(gtalignDict[key],  columns=['Reference_description', 'Reference_length-normalized_TM-score', 'Query_length-normalized_TM-score', 'RMSD', '#Aligned_residues', 'Query_alignment_boundaries','Reference_alignment_boundaries','Reference_length'])
  temp_table.insert(0, "Query_description", key)
  # print(temp_table.info())
# add this table to the previous table if doing multiple files
  gtalign_table = pd.concat([gtalign_table, temp_table], ignore_index=True, axis=0)
  # print('=======================================CONCAT=========================================')
  # print(gtalign_table.info())
# convert string to float for manipulation
  gtalign_table['Query_length-normalized_TM-score'] = gtalign_table['Query_length-normalized_TM-score'].astype(float)

gtalign_table.to_csv('gtalign_table',index=False)
