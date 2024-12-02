#!/bin/bash
#SBATCH --output Manual%j.out
#SBATCH --job-name Manual
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32

snakemake -s ./snakemake/preprocess.smk --unlock
snakemake -s ./snakemake/Manual.smk --configfile ./snakemake/config.yaml -j 180