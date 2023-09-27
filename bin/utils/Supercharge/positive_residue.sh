#!/bin/bash
#SBATCH --output positive_residue.%j.out
#SBATCH --job-name positive_residue
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
mkdir -p /share/home/cheny/Projects/Supercharge/data/RBD/Supercharge/positive_residue

time mpirun -n 5 $ROSETTA_BIN/supercharge.mpi.linuxgccrelease @/share/home/cheny/Projects/Supercharge/rosetta/positive_residue.flags
