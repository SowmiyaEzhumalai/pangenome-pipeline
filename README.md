# 🧬 Pangenome Pipeline

A reproducible, Snakemake-based pipeline for bacterial pangenome construction and analysis. This workflow automates genome annotation with **Prokka**, pangenome clustering with **Roary**, visualization of core,accessory and unique gene distributions, and gene list extraction - all managed via isolated Conda environments.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Pipeline Workflow](#pipeline-workflow)
- [Repository Structure](#repository-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Output](#output)
- [Samples](#samples)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)
- [References](#references)

---

## Overview

Pangenomics compares gene content across multiple strains of a species to identify:

- **Core genome** — genes present in all strains (conserved functions)
- **Accessory genome** — genes present in some but not all strains (flexible functions)
- **Unique genes** — genes found in only one strain (strain-specific features)

This pipeline processes 42 *Pediococcus acidilactici* genome assemblies through a fully automated workflow, producing a presence-absence matrix, phylogenetic tree, and categorised gene lists.

---

## Pipeline Workflow

```
FASTA Genomes (per strain)
        │
        ▼
┌───────────────────┐
│  Prokka Annotation │  ← Predicts genes, generates GFF files
└───────────────────┘
        │
        ▼
┌───────────────────┐
│   Roary (Pangenome)│  ← Clusters genes at ≥60% identity across all strains
└───────────────────┘
        │
        ├──────────────────────────────────────┐
        ▼                                      ▼
┌───────────────────┐              ┌───────────────────────┐
│   Roary Plots      │              │  Gene List Extraction  │
│  - Matrix          │              │  - core_genes.csv      │
│  - Pie chart       │              │  - accessory_genes.csv │
│  - Frequency plot  │              │  - unique_genes.csv    │
└───────────────────┘              └───────────────────────┘
```

---

## Repository Structure

```
pangenome-pipeline/
├── Snakefile                  # Main workflow definition
├── config.yaml                # Sample list configuration
├── envs/
│   ├── prokka.yaml            # Conda environment for Prokka
│   ├── roary.yaml             # Conda environment for Roary
│   └── roary_plots.yaml       # Conda environment for plotting scripts
├── scripts/
│   ├── roary_plots.py         # Generates pangenome visualisations
│   └── core_access_uniq_genes.py  # Splits gene presence-absence matrix
└── Nucleotide_Files_Fasta_Format/  # Input genome FASTAs (not tracked in git)
```

---

## Requirements

- **OS:** Linux or macOS
- **Snakemake:** ≥ 7.0
- **Conda / Mamba:** for environment management (Mamba recommended for speed)

> All tool dependencies (Prokka, Roary, Python packages) are installed automatically via the `envs/` Conda environments.

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/SowmiyaEzhumalai/pangenome-pipeline.git
cd pangenome-pipeline
```

**2. Install Snakemake** (if not already installed)

```bash
conda create -n snakemake -c bioconda -c conda-forge snakemake mamba
conda activate snakemake
```

**3. Place input genomes**

Put your genome FASTA files (`.fasta`) into the `Nucleotide_Files_Fasta_Format/` directory. Filenames should match the sample names listed in `config.yaml`.

```
Nucleotide_Files_Fasta_Format/
├── 13_7.fasta
├── A1602.fasta
├── AF2019.fasta
└── ...
```

---

## Configuration

Edit `config.yaml` to list the sample names you want to include:

```yaml
samples:
  - "13_7"
  - "A1602"
  - "AF2019"
  # add or remove samples here
```

The pipeline automatically detects FASTA files in `Nucleotide_Files_Fasta_Format/` matching these names.

---

## Usage

**Dry run** (check what steps will execute without running them):

```bash
snakemake -n --use-conda --configfile config.yaml
```

**Full run** (uses all available cores):

```bash
snakemake --use-conda --cores all --configfile config.yaml
```

**Run with a specific number of threads:**

```bash
snakemake --use-conda --cores 16 --configfile config.yaml
```

**Run on an HPC cluster (SLURM example):**

```bash
snakemake --use-conda --cores 64 \
  --cluster "sbatch --mem={resources.mem_mb}M --cpus-per-task={threads} --time=04:00:00" \
  --jobs 20
```

---

## Output

| Path | Description |
|------|-------------|
| `prokka/{sample}/{sample}.gff` | Prokka annotation per strain |
| `roary_output/gene_presence_absence.csv` | Full pangenome presence-absence matrix |
| `roary_output/accessory_binary_genes.fa.newick` | Accessory genome phylogenetic tree |
| `roary_output/roary_plots/pangenome_matrix.png` | Heatmap of gene presence across strains |
| `roary_output/roary_plots/pangenome_pie.png` | Pie chart of core/accessory/unique breakdown |
| `roary_output/roary_plots/pangenome_frequency.png` | Frequency histogram of gene conservation |
| `gene_lists/core_genes.csv` | Genes present in **all** strains |
| `gene_lists/accessory_genes.csv` | Genes present in **some** strains |
| `gene_lists/unique_genes.csv` | Genes present in **one** strain only |

---

## Samples

This pipeline was validated on 42 *Pediococcus acidilactici* strains, including:

- FDAARGOS reference strains (1007, 1008, 1133)
- SRCM collection strains (100313, 100424, 101189, 102024, 102731, 102732, 103367, 103387, 103444)
- ATCC 8042 reference strain
- Additional environmental and clinical isolates

See [`config.yaml`](config.yaml) for the full sample list.

---

## Contributing

Contributions and suggestions are welcome. Please open an [issue](https://github.com/SowmiyaEzhumalai/pangenome-pipeline/issues) or submit a pull request.


---

## Acknowledgements

This pipeline relies on the following open-source tools:

- [Prokka](https://github.com/tseemann/prokka) — rapid prokaryotic genome annotation
- [Roary](https://sanger-pathogens.github.io/Roary/) — fast large-scale prokaryote pan genome analysis
- [Snakemake](https://snakemake.readthedocs.io/) — workflow management system
- [roary_plots.py](https://github.com/sanger-pathogens/Roary/blob/master/contrib/roary_plots/roary_plots.py) — pangenome visualisation script

## References

PANGENOME

- Golchha N.C., Nighojkar A. & Nighojkar S. 2024. Bacterial pangenome: A review on the current strategies, tools and applications. Medinformatics. . https://doi.org/10.47852/bonviewMEDIN42022496
- Matthews, C. A., Watson-Haigh, N. S., Burton, R. A., & Sheppard, A. E. (2024). A gentle introduction to pangenomics. Briefings in bioinformatics, 25(6), bbae588. https://doi.org/10.1093/bib/bbae588

SNAKEMAKE
- Köster J. & Rahmann S. 2012. Snakemake--a scalable bioinformatics workflow engine. Bioinformatics. 28: 2520–2522. https://doi.org/10.1093/bioinformatics/bty350

PROKKA
- Seemann T. 2014. Prokka: rapid prokaryotic genome annotation. Bioinformatics. 30: 2068–2069. https://doi.org/10.1093/bioinformatics/btu153

ROARY
- Page A.J., Cummins C.A., Hunt M., Wong V.K., Reuter S., Holden M.T.G., Fookes M., Falush D., Keane J.A. & Parkhill J. 2015. Roary: rapid large-scale prokaryote pan genome analysis. Bioinformatics. 31: 3691–3693. https://doi.org/10.1093/bioinformatics/btv421




