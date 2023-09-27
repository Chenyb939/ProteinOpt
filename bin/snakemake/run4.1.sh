#!/bin/bash
#SBATCH --output Super_file%j.out
#SBATCH --job-name Super_file
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=32

snakemake -s snakefile4.1.smk -j 32