import csv
from Bio import SeqIO
import sys
import os

# Get file paths from command-line arguments
reference_fasta = sys.argv[1]
core_genes_file = sys.argv[2]
accessory_genes_file = sys.argv[3]
unique_genes_file = sys.argv[4]

# Output file paths
core_fasta = "fasta_seq/core_genes.fasta"
accessory_fasta = "fasta_seq/accessory_genes.fasta"
unique_fasta = "fasta_seq/unique_genes.fasta"

# Create output directory if it doesn't exist
os.makedirs("fasta_seq", exist_ok=True)

# Function to read gene list from CSV file
def read_gene_list(file_path):
    genes = []
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            genes.append(row[0].strip())  # assuming single column of gene names
    return genes

# Read the gene lists
core_genes = read_gene_list(core_genes_file)
accessory_genes = read_gene_list(accessory_genes_file)
unique_genes = read_gene_list(unique_genes_file)

# Function to extract sequences from FASTA
def extract_sequences(fasta_file, gene_list, output_file):
    # Load the reference genome
    reference_genome = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))
    
    with open(output_file, "w") as out_file:
        for gene in gene_list:
            gene_found = False  # Flag to check if gene is found in the reference genome
            # Check for exact match or partial match (e.g., gene name without version or description)
            for header in reference_genome:
                if gene == header.split()[0]:  # Match gene name (ignore extra parts after space)
                    seq = reference_genome[header].seq
                    out_file.write(f">{header}\n{seq}\n")
                    gene_found = True
                    break
            if not gene_found:
                print(f"Warning: Gene {gene} not found in the reference genome.")

# Extract sequences for each gene list
extract_sequences(reference_fasta, core_genes, core_fasta)
extract_sequences(reference_fasta, accessory_genes, accessory_fasta)
extract_sequences(reference_fasta, unique_genes, unique_fasta)

print("Gene extraction completed.")

