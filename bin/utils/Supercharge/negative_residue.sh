#!/bin/bash
#SBATCH --output negative_residue.%j.out
#SBATCH --job-name negative_residue
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
mkdir -p /share/home/cheny/Projects/Supercharge/data/RBD/Supercharge/negative_residue

time mpirun -n 5  $ROSETTA_BIN/supercharge.mpi.linuxgccrelease  @/share/home/cheny/Projects/Supercharge/rosetta/negative_residue.flags