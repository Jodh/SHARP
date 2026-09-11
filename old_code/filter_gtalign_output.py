# check if returned matches overlap with the queries at their duf regions, then if yes, check if size of match is large enough
import sys
import csv
#import matplotlib.pyplot as plt
#import numpy as np

input_file1 = sys.argv[1]
input_file2 = sys.argv[2]
output_file = sys.argv[3]

# need a list of DUF regions for each query
def get_boundaries_and_DUF(queries):
    with open(queries, 'r') as infile:
        f = csv.reader(infile)
        next(f) # skip header
        # output a dictionary that can be used as look up for d1,d2 values for our overlap calculations
        boundary_dict = {}
        for row in f:
            #print(row)
            value = [int(row[2]),int(row[3]),row[1]]
            key = row[0]
            boundary_dict[key] = value
    return boundary_dict

def overlap(q1,q2,d1,d2):
    # check if matched region overlaps with DUF region
    # we know q2 > q1 and d2 > d1
    if q1 > d2 or d1 > q2:
        return False
    else:
        return True

def read_queries(query1, query2, overlap_ratio=0.5, length=5):
    boundary_dict = get_boundaries_and_DUF(query2)

    with open(query1, 'r') as infile:
        f = csv.reader(infile)
        next(f) # skip header
        print("CGene,DUF,overlap_boundary,DUF_boundary,match,overlap_fraction,TMscore_match-length-normalized,TMscore_query-length-nomalized,RMSD")
        for row in f:
            # get the required inputs for math
            q1q2 = row[6].split('-')
            q1 = int(q1q2[0])
            q2 = int(q1q2[1])
            d1,d2,duf = boundary_dict[row[0]]
            #print(q2-q1+1)

            # do math to check overlap
            if overlap(q1,q2,d1,d2):
                inputs = [q1,q2,d1,d2]
                inputs.sort()
                overlap_fraction = (inputs[2]-inputs[1]+1)/(d2-d1+1)
                if overlap_fraction >= overlap_ratio:
            # is match a significant fraction of the duf, remove matches that are too small, because gtalign picks and aligns matches with the query sequences that are far larger than the absolute length of the match
                    if 10*int(row[8]) >= length*(d2-d1):
                        print("{},{},{}-{},{}-{},{},{},{},{},{}".format(row[0],duf,q1,q2,d1,d2,row[1],overlap_fraction, row[2], row[3], row[4]))
            #else:
                #print(row[0],q1,'-',q2, d1,'-',d2, row[1], 0)

# deal with the fact that number of matched residues may be much smaller than the size of the full region that matched. This results in very small candidate proteins that dont provide any useful information but clutter the output

# find ratio of residues that actually matched over total size of matched region in gtalign table
def matched_residue_ratio(query1):
    X = []
    with open(query1, 'r') as infile:
        f = csv.reader(infile)
        next(f) # skip header
        for row in f:
            q1q2 = row[6].split('-')
            q1 = int(q1q2[0])
            q2 = int(q1q2[1])
            #X.append(((q2-q1)-int(row[8]))/(q2-q1)*100)
            X.append(((q2-q1)-int(row[5]))/(q2-q1))
    return X

# make graph for matched residue ratio
def display_ratio_hist(X):
    n_bins = 20
    fig, axis = plt.subplots()
    axis.hist(X, bins=n_bins)
    plt.savefig('residue_ratio_hist.png')

def display_ratio(X):
    x = np.arange(1,len(X)+1,1)
    fig, axis = plt.subplots()
    axis.plot(x, X)
    axis.grid()
    fig.savefig('residue_ratio.png')

if __name__ == '__main__':
    read_queries(input_file1, input_file2, overlap_ratio=0.5, length=5)
    # testing functions
    #get_boundaries(input_file2)
    # display graph
    #display_ratio_hist(matched_residue_ratio(input_file1))
    #display_ratio(matched_residue_ratio(input_file1))
