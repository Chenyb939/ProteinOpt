#!/bin/bash
#SBATCH --output Supercharge%j.out
#SBATCH --job-name Supercharge
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32

snakemake -s ./snakemake/preprocess.smk --unlock
snakemake -s ./snakemake/Supercharge_ref.smk --configfile ./snakemake/config.yaml -j 180