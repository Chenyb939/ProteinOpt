#!/bin/bash
#SBATCH --output VIP%j.out
#SBATCH --job-name VIP
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
mkdir -p /share/home/cheny/Projects/VIP/data/RBD/VIP

time mpirun -n 5 $ROSETTA_BIN/vip.mpi.linuxgccrelease @/share/home/cheny/Projects/VIP/rosetta/VIP.flags