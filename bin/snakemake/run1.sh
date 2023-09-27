#!/bin/bash
#SBATCH --output PER%j.out
#SBATCH --job-name PER
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=32

snakemake -s snakefile.smk -j 32