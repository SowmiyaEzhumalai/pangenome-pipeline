
import os
from pathlib import Path

FASTA_DIR = "Nucleotide_Files_Fasta_Format"
PROKKA_DIR = "prokka"
ROARY_DIR = "roary_output"
GENE_DIR = "gene_lists"

# List all genome names from FASTA files
genomes = [f.stem for f in sorted(Path(FASTA_DIR).glob("*.fasta"))]

# Rule: Final target – wait for Roary output and plots
rule all:
    input:
        f"{ROARY_DIR}/gene_presence_absence.csv",
        f"{ROARY_DIR}/roary_plots/pangenome_matrix.png",
        f"{ROARY_DIR}/roary_plots/pangenome_pie.png",
        f"{ROARY_DIR}/roary_plots/pangenome_frequency.png",
        f"{GENE_DIR}/core_genes.csv",
        f"{GENE_DIR}/accessory_genes.csv",
        f"{GENE_DIR}/unique_genes.csv"

# Rule: Prokka annotation for each genome
rule prokka_annotation:
    input:
        fasta = f"{FASTA_DIR}/{{sample}}.fasta"
    output:
        gff = f"{PROKKA_DIR}/{{sample}}/{{sample}}.gff"
    conda:
        "envs/prokka.yaml"
    threads: 4
    shell:
        """
        prokka --cpus {threads} --force --kingdom Bacteria --genus "Pediococcus" --species "acidilactici" \
        --locustag {wildcards.sample} --addgenes --outdir {PROKKA_DIR}/{wildcards.sample} \
        --prefix {wildcards.sample} {input.fasta}
        """

# Rule: Run Roary on all GFF files
rule run_roary:
    input:
        gffs = expand(f"{PROKKA_DIR}/{{sample}}/{{sample}}.gff", sample=genomes)
    output:
        spreadsheet = f"{ROARY_DIR}/gene_presence_absence.csv",
        tree = f"{ROARY_DIR}/accessory_binary_genes.fa.newick"
    conda:
        "envs/roary.yaml"
    threads: 8
    shell:
        """
        rm -rf {ROARY_DIR}
        roary -e --mafft -p {threads} -i 60 -f {ROARY_DIR} {input.gffs}
        """

# Rule: Generate Roary plots
rule roary_plots:
    input:
        tree = f"{ROARY_DIR}/accessory_binary_genes.fa.newick",
        spreadsheet = f"{ROARY_DIR}/gene_presence_absence.csv"
    output:
        plots_matrix = touch(f"{ROARY_DIR}/roary_plots/pangenome_matrix.png"),
        plots_pie = touch(f"{ROARY_DIR}/roary_plots/pangenome_pie.png"),
        plots_freq = touch(f"{ROARY_DIR}/roary_plots/pangenome_frequency.png")
    conda:
        "envs/roary_plots.yaml"
    log:
        f"{ROARY_DIR}/roary_plots.log"
    shell:
        """
        mkdir -p {ROARY_DIR}/roary_plots
        python -W ignore scripts/roary_plots.py {input.tree} {input.spreadsheet} > {log} 2>&1
        """

# Rule: Split Core, accessory and unique genes
rule core_access_uniq_split:
    input:
        spreadsheet = f"{ROARY_DIR}/gene_presence_absence.csv"
    output:
        core = "gene_lists/core_genes.csv",
        accessory = "gene_lists/accessory_genes.csv",
        unique = "gene_lists/unique_genes.csv"
    conda:
        "envs/roary_plots.yaml" 
    shell:
        """
        mkdir -p gene_lists
        python scripts/core_access_uniq_genes.py {input.spreadsheet} {output.core} {output.accessory} {output.unique}
        """

