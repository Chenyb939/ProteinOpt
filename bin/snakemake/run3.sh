#!/bin/bash
#SBATCH --output DMS%j.out
#SBATCH --job-name DNS
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=32

snakemake -s snakefile3.smk -j 32