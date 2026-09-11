# Documentation
## What is Structural Homology Assisted search for Related Proteins (SHARP)?
Aim of SHARP is to provide a series of steps that can assist scientists to find possible functions of unknown genes. We leverage the fact that proteins with similar 3d structures will have similar functions.

The pipeline is divided logically into a data layer and a process layer. The initial input and its subsequent transformations as it goes through the pipeline are visible in this layer. The process layer contains all the tools and algorithms that are responsible for transforming the input sequence into the final function ranking list. We also divide the pipeline chronologically into the pre-processing, labelling and ranking stages. This keeps the whole process modular. The jupyter notebook provided with the paper can be easily customized. The pipeline is capable of both large scale and single protein functional enrichment.

<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/932f2245-84f7-43e5-a1ae-5796b74a6ed4" />


## Pre-Processing
### Data Layer
**Input:** The protein(s) sequence with domains of unknown function.

**Output:** Target proteins that are structurally similar to the query protein. A tab separated file.
### Process Layer
This subsection of the pipeline involves using alphafold3 to predict the structures of the query protein and then using that structure to find target proteins using Foldseek. Installation of both alphafold3 and foldseek is going to be unique for each user and thus this process cannot be automated in our pipeline. But a separate jupyter notebook is provided for mass processing and download of alphafold structures for large scale protein functional analysis. We also provide foldseek commands used for our analysis.
Foldseek does not provide functional information for the target proteins found and thus the next part of the pipeline is labelling these proteins.
## Function Labelling
### Data Layer
**Input:** List of target proteins in a tab separated file.

**Output:** List of target proteins labeled with functional information in a tabular file, a json file containing the same information for easy computation in the future steps.
### Process Layer
Using the uniprot API rich functional information is extracted for each target protein. Uniprot has information about domains for most proteins. This includes description and position of each domain for that protein. We also assign a weight to each of these domain descriptions. This weight has a range from 0 to 1. The weight is calculated as the fraction of overlap of each domain of the target protein with the aligned region on the query protein. 0 represents no overlap and a 1 means that the domain of the target protein is fully inside the aligned region of the query protein.  The weight information is later used in the ranking process.
## Aggregating and Ranking
### Data Layer
**Input:** List of target proteins labeled with functional information in a tabular file.

**Output:** List of possible functions assigned to the query protein, ranked from most likely to least likely.
### Process Layer
This stage aggregates the function descriptions from the input by counting all descriptions that match multiplied by their weights. Thus all unique descriptions from the target proteins are ranked by their number of occurrences weighted by their overlap with the aligned region in the query protein. For example if there are 5 target proteins for a query and 3 of them have the description “H-Box” and weights of 0.5, 0.7, 1.0 respectively and 2 of them have the description “DEAD box” with weights 0.2, 0.4 respectively then the final ranked list will be H-Box: 2.2, DEAD box: 0.6.

## Instructions for Running SHARP
### Install Jupyter Notebook
Using the command `pip install notebook` to install jupyter notebook on your computer. This is needed to run the `SHARP.ipynb` file.
### Download SHARP.ipynb
Run Jupyter Notebook which is needed to run `SHARP.ipynb`, using the command `jupyter notebook`. This will open your web browser with a directory like interface. Find the location of `SHARP.ipynb` where ever it was downloaded. Click on it to run it. It will open another tab on your browser with SHARP ready to run.
### Help for the Pre-processing Step
In its current iteration, the pipeline expects the user to have access to a local foldseek installation and also have the .pdb model for the protein you wish to query. I have provided a short step by step guide to work with foldseek once you have it installed.

1. Install on Linux system through `conda install -c conda-forge -c bioconda foldseek`. For more details check https://github.com/steineggerlab/foldseek

2. Download the database you want to search in (swissprot by default):

`foldseek databases Alphafold/Swiss-Prot sp tmp`

command template:

`foldseek databases <address to the database on foldseek's servers> <custom_name> <tmp folder name>`

3. create index from downloaded database
(skip this step if doing large batch queries)

`foldseek createindex sp tmp`


4. search the database and produce 

`foldseek easy-search A0A015LDT9.pdb sp aln tmp --format-output query,target,qstart,qend,tstart,tend,alntmscore,qtmscore,ttmscore,lddt,prob,evalue`

This will produce a file called `aln` for the protein model `A0A015LDT9.pdb` with columns arranged according to the `format-output` option. This `aln` file will be the input for the SHARP pipeline.

command template:

`foldseek easy-search <input.pdb> <db_name> <outfile_name> <tmp folder> <output format options>`
 



