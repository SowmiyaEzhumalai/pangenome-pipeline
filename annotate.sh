#!/bin/bash

annot_dir="prokka1"
fasta_dir="Nucleotide_Files_Fasta_Format"
extension=".fasta"
cpus=8

mkdir -p ${annot_dir}

allfasta=("${fasta_dir}"/*"${extension}")

for file in ${allfasta[@]}
do
bname=$(basename $file ${extension})

prokka --cpus $cpus --kingdom Bacteria --genus "Pediococcus" --species "acidilactici" --locustag $bname \
--addgenes --outdir ${annot_dir}/${bname} --prefix ${bname} $file
done
