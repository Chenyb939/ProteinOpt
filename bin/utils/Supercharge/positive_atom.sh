#!/bin/bash
#SBATCH --output positive_atom.%j.out
#SBATCH --job-name positive_atom
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
mkdir -p /share/home/cheny/Projects/Supercharge/data/RBD/Supercharge/positive_atom

time mpirun -n 5 $ROSETTA_BIN/supercharge.mpi.linuxgccrelease @/share/home/cheny/Projects/Supercharge/rosetta/positive_atom.flags