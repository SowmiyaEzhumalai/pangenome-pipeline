import pandas as pd
import sys

# Step 1: Read command-line arguments
input_file = sys.argv[1]
core_out = sys.argv[2]
accessory_out = sys.argv[3]
unique_out = sys.argv[4]

# Step 2: Load the gene_presence_absence.csv
df = pd.read_csv(input_file)

# Step 3: Determine number of isolates from strain columns (starting from column 15)
strain_columns = df.columns[14:]
num_isolates = len(strain_columns)
df["Isolate_Count"] = df[strain_columns].notna().sum(axis=1)

# Step 4: Classify genes
core_genes = df[df["Isolate_Count"] == num_isolates][["Gene", "Annotation"]]
unique_genes = df[df["Isolate_Count"] == 1][["Gene", "Annotation"]]
accessory_genes = df[(df["Isolate_Count"] > 1) & (df["Isolate_Count"] < num_isolates)][["Gene", "Annotation"]]

# Step 5: Save outputs
core_genes.to_csv(core_out, index=False)
accessory_genes.to_csv(accessory_out, index=False)
unique_genes.to_csv(unique_out, index=False)
