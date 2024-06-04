#!/bin/bash
#SBATCH --output Manual%j.out
#SBATCH --job-name Manual
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32

snakemake -s Manual.smk -j 32