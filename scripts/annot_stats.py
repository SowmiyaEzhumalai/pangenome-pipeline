import pandas as pd
import sys
import glob
import os

maindir = sys.argv[1]  # Get main directory from command-line argument
allfiles = glob.glob(f'{maindir}/*/*.tsv')  # Find all .tsv files in subdirectories
maindf = []

for file_ in allfiles:
    bname = os.path.basename(file_).replace('.tsv', '')  # Extract filename without extension
    print(f"Processing: {bname}")  # Print the file being processed
    
    df = pd.read_csv(file_, sep='\t')  # Read the TSV file into a DataFrame
    
    featurecounts = df['ftype'].value_counts()  # Count occurrences of each feature type
    
    res = pd.DataFrame(featurecounts)  # Create DataFrame from value counts
    res.columns = [bname]  # Rename the column to match the filename
    
    maindf.append(res)  # Append to list
    
# Merge all DataFrames and save as CSV
out = pd.concat(maindf, axis=1)
out.to_csv('prokka_summary.csv')

print("Annotation summary saved as prokka_summary.csv")
