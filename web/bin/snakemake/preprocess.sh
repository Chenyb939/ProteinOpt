#!/bin/bash
#SBATCH --output preprocess%j.out
#SBATCH --job-name preprocess
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32

snakemake -s preprocess.smk -j 32