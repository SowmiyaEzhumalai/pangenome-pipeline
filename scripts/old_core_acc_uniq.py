'''
import pandas as pd

# Load the gene_presence_absence.csv
file_path = "/roary_output/gene_presence_absence.csv"
df = pd.read_csv(file_path)

# Determine number of genomes/isolates from presence/absence columns
# Columns from the 15th column onward are usually the per-strain columns in Roary output
strain_columns = df.columns[14:]
num_isolates = len(strain_columns)

# Count how many isolates have each gene (non-NaN entries in strain columns)
df["Isolate_Count"] = df[strain_columns].notna().sum(axis=1)

# Separate into categories
core_genes = df[df["Isolate_Count"] == num_isolates][["Gene", "Annotation"]]
unique_genes = df[df["Isolate_Count"] == 1][["Gene", "Annotation"]]
accessory_genes = df[(df["Isolate_Count"] > 1) & (df["Isolate_Count"] < num_isolates)][["Gene", "Annotation"]]

# Save to CSV files
core_genes.to_csv("/gene_lists/core_genes.csv", index=False)
accessory_genes.to_csv("/gene_lists/accessory_genes.csv", index=False)
unique_genes.to_csv("/gene_lists/unique_genes.csv", index=False)
'''
import pandas as pd
import sys

# Get command-line arguments from Snakemake
input_file = sys.argv[1]
core_out = sys.argv[2]
accessory_out = sys.argv[3]
unique_out = sys.argv[4]

# Load the gene_presence_absence.csv
df = pd.read_csv(input_file)

# Determine number of genomes/isolates from presence/absence columns
strain_columns = df.columns[14:]
num_isolates = len(strain_columns)

# Count how many isolates have each gene
df["Isolate_Count"] = df[strain_columns].notna().sum(axis=1)

# Split into categories
core_genes = df[df["Isolate_Count"] == num_isolates][["Gene", "Annotation"]]
unique_genes = df[df["Isolate_Count"] == 1][["Gene", "Annotation"]]
accessory_genes = df[(df["Isolate_Count"] > 1) & (df["Isolate_Count"] < num_isolates)][["Gene", "Annotation"]]

# Save outputs to paths provided by Snakemake
core_genes.to_csv(core_out, index=False)
accessory_genes.to_csv(accessory_out, index=False)
unique_genes.to_csv(unique_out, index=False)

