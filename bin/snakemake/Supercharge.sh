#!/bin/bash
#SBATCH --output Supercharge_ref%j.out
#SBATCH --job-name Supercharge_ref
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32

snakemake -s ./snakemake/preprocess.smk --unlock
snakemake -s ./snakemake/Supercharge.smk --configfile ./snakemake/config.yaml -j 180