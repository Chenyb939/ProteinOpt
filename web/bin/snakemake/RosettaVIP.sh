#!/bin/bash
#SBATCH --output RosettaVIP%j.out
#SBATCH --job-name RosettaVIP
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32

snakemake -s RosettaVIP.smk -j 32