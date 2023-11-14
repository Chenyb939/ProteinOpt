#!/bin/bash
#SBATCH --output Supercharge%j.out
#SBATCH --job-name Supercharge
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32

snakemake -s Supercharge.smk -j 32