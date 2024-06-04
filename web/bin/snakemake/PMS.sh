#!/bin/bash
#SBATCH --output PMS%j.out
#SBATCH --job-name PMS
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32

snakemake -s PMS.smk -j 32