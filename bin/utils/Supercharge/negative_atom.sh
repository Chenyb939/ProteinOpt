#!/bin/bash
#SBATCH --output negative_atom.%j.out
#SBATCH --job-name negative_atom
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
mkdir -p /share/home/cheny/Projects/Supercharge/data/RBD/Supercharge/negative_atom

time mpirun -n 5 $ROSETTA_BIN/supercharge.mpi.linuxgccrelease @/share/home/cheny/Projects/Supercharge/rosetta/negative_atom.flags