# This script uses the uniprot API to grab interpro families and add it to the input table.

import requests, sys, json, numpy as np
import csv

#input_table = '/home/jodh/scripts/small_scripts/gtalign_overlap_50_50.csv'
#out_table = '/home/jodh/scripts/small_scripts/gtalign_overlap_50_50_with_family.csv'

input_table = sys.argv[1]
out_table = sys.argv[2]

def get_matchIDs(input_table):
    match_IDs = []
    with open(input_table, 'r') as infile:
        f = csv.reader(infile)
        next(f)
        for row in f:
            match_IDs.append(row[4])
    return match_IDs

def get_interpro_name(matchID):
    params = {"fields": ["xref_interpro"]}
    headers = {"accept": "application/json"}
    base_url = "https://rest.uniprot.org/uniprotkb/{}".format(matchID)

    response = requests.get(base_url, headers=headers, params=params)
    if not response.ok:
        #response.raise_for_status()
        family_name = '"Invalid Request"'
        return family_name
        #sys.exit()

    data = response.json()
    #print(matchID)
    #print(type(json.dumps(data['uniProtKBCrossReferences'], indent=2)), len(json.dumps(data['uniProtKBCrossReferences'], indent=2)))
    try:

        if len(json.dumps(data['uniProtKBCrossReferences'], indent=2)) > 2:
            family_name = json.dumps(data['uniProtKBCrossReferences'][0]['properties'][0]['value'], indent=2)
        else:
            family_name = '"None"'
    except:
        family_name = '"None"'
    return family_name

def append_family_to_input_table(input_table, out_table):
    family_names = []
    match_IDs = get_matchIDs(input_table)
    for match_ID in match_IDs:
        family_names.append(get_interpro_name(match_ID))

    with open(input_table, 'r') as infile, open(out_table, 'w') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        headers = next(reader)
        headers.append('family')
        writer.writerow(headers)

        for i, row in enumerate(reader):
            row.append(family_names[i].split('"')[1])
            writer.writerow(row)

def clean_table(input_table,output_table):
    with open(input_table, 'r') as infile, open(output_table, 'w') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)
        writer.writerow(header)

        for row in reader:
            family = row[9].split('"')[1]
            row[9] = family
            # remove all """'s from 9th element in the row and reattach the clean family name
            #print(row)
            writer.writerow(row)

if __name__ == '__main__':
    append_family_to_input_table(input_table, out_table)

