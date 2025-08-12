import sys
import pandas as pd
from Bio import SeqIO

# Read Command line arguments
reference_fasta = sys.argv[1]
core_csv = sys.argv[2]
accessory_csv = sys.argv[3]
unique_csv = sys.argv[4]

# Outputs
core_fasta = sys.argv[5]
accessory_fasta = sys.argv[6]
unique_fasta = sys.argv[7]

# Load all sequences into a lookup dictionary: {gene_name : SeqRecord}
seq_records = {}
for record in SeqIO.parse(reference_fasta, "fasta"):
    parts = record.description.split()
    if len(parts) > 1:
        gene_name = parts[1]  # <-- second word
        seq_records[gene_name] = record

def write_genes(csv_file, output_fasta):
    df = pd.read_csv(csv_file)
    genes = set(df["Gene"].str.strip())

    matched = []
    missing = []

    for gene in genes:
        if gene in seq_records:
            matched.append(seq_records[gene])
        else:
            missing.append(gene)

    if missing:
        print(f"Missing {len(missing)} genes from {csv_file}:")
        for mg in missing:
            print(mg)

    with open(output_fasta, "w") as out_f:
        SeqIO.write(matched, out_f, "fasta")

# Process each file
write_genes(core_csv, core_fasta)
write_genes(accessory_csv, accessory_fasta)
write_genes(unique_csv, unique_fasta)

