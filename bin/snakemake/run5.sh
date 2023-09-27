#!/bin/bash
#SBATCH --output VIP%j.out
#SBATCH --job-name VIP
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32

snakemake -s snakefile5.smk -j 32