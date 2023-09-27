#!/bin/bash
#SBATCH --output PM%j.out
#SBATCH --job-name PM
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=32

snakemake -s snakefile2.smk -j 32