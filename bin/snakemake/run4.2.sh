#!/bin/bash
#SBATCH --output Super_ref%j.out
#SBATCH --job-name Super_ref
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=32

snakemake -s snakefile4.2.smk -j 32