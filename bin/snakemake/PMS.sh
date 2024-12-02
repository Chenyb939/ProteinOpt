#!/bin/bash
#SBATCH --output PMS%j.out
#SBATCH --job-name PMS
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32

snakemake -s ./snakemake/preprocess.smk --unlock
snakemake -s ./snakemake/PMS.smk --configfile ./snakemake/config.yaml -j 180