import os
import argparse
import numpy as np
import pandas as pd
from Bio import PDB
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
from pyrosetta import pose_from_pdb, init
from pyrosetta.rosetta.core.select.residue_selector import NeighborhoodResidueSelector, ResidueIndexSelector

def get_neighborhood(pdbpath, site_list, dist):
    init()
    pose = pose_from_pdb(pdbpath)
    site_lst = []
    for site in site_list:
        residue_selector = ResidueIndexSelector(site)
        nbr_selector = NeighborhoodResidueSelector(residue_selector, round(dist,1), True)
        site = nbr_selector.apply(pose)

        for i in range(len(list(site))):
            if list(site)[i] is True:
                site_lst.append(i + 1)
    out_lst = list(set(site_lst))
    return out_lst

def generate_com(out_list, chain):
    out = ''
    for i in out_list:
        out += f'{i}{chain},'
    return out[:-1]

def clean_out(input_lst, out_lst, max_len, chain):  # site arround select pose
    clean_lst = [int(i.replace(chain, '')) for i in input_lst]
    fin_lst = [i for i in out_lst if i not in clean_lst]
    return [i for i in fin_lst if i <= max_len]

def clean_out_pos(input_lst, out_lst, max_len, chain):  # site arround select pose with selected
    # clean_lst = [int(i.replace(chain, '')) for i in input_lst]
    # fin_lst = [i for i in out_lst if i not in clean_lst]
    return [i for i in out_lst if i <= max_len]

def neighbor(pdbpath, site_list, dist, max_len, chain):
    out_lst = get_neighborhood(pdbpath, site_list, dist)
    out_lst.sort()
    out_lst = clean_out_pos(site_list, out_lst, max_len, chain)
    out = generate_com(out_lst, chain)
    return out


def get_mutant_pos(input1, input2, chain):
    old_chain_lst = []
    old_seq_lst = []
    new_chain_lst = []
    new_seq_lst = []
    parser = PDB.PDBParser()
    structure = parser.get_structure('old', input1)
    ppb = PDB.PPBuilder()
    for pp in ppb.build_peptides(structure):
        old_seq_lst.append(pp.get_sequence())
    for i in structure[0]:
        old_chain_lst.append(str(i).split('id=')[-1].replace('>', ''))

    parser = PDB.PDBParser()
    structure = parser.get_structure('new', input2)
    ppb = PDB.PPBuilder()
    for pp in ppb.build_peptides(structure):
        new_seq_lst.append(pp.get_sequence())
    for i in structure[0]:
        new_chain_lst.append(str(i).split('id=')[-1].replace('>', ''))

    seq1 = old_seq_lst[old_chain_lst.index(chain)]
    seq2 = new_seq_lst[new_chain_lst.index(chain)]
    alignments = pairwise2.align.globalxx(seq1, seq2)
    res = format_alignment(*alignments[-1])

    pos_lst = []
    for index, value in enumerate(res.split('\n')[1]):
        if value == '.':
            pos_lst.append(index + 1)
    pos_lst.sort(reverse=False)
    pos_lst_new = [str(i) + chain for i in pos_lst]
    return pos_lst_new


def gene_compm(shell_path, name, node, ntasks, input_path, wt_path, out_path, xml_path, ref_path, num, neig, chain):
    with open(os.path.join(shell_path), 'w') as file:
        # file.write(f'#!/bin/bash\n#SBATCH --output {name}%j.out\n#SBATCH --job-name {name}\n#SBATCH --nodes={node}\n#SBATCH --ntasks-per-node={ntasks}\n')
        file.write(f'mpirun -n {node*ntasks} $ROSETTA_BIN/rosetta_scripts.mpi.linuxgccrelease -s {input_path} -in:file:native {wt_path} -out:path:pdb {out_path} -out:path:score {out_path} -linmem_ig 10 -nstruct {num} -parser:protocol {xml_path} -parser:script_vars resfile={ref_path} multichain={chain} multiposition={neig} bonusvalue=2.25')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Generate xml file for mutation')
    parser.add_argument('--wt_path', type=str, default='./6yz5.pdb', help='WT pdb file')
    parser.add_argument('--super_path', type=str, default='./6yz5.pdb', help='supercharge generated pad file path')
    parser.add_argument('--distance', type=float, default=7.0, help='The distance around target amino acids')
    parser.add_argument('--chain', type=str, default='E', help='chain to design')
    parser.add_argument('--start_pos', type=int, default=334, help='The first residue position of the chain to be designed in the pdb file')
    parser.add_argument('--end_pos', type=int, default=528, help='The last residue position of the chain to be designed in the pdb file')
    parser.add_argument('--shell_path', type=str, default='./', help='shell path')
    parser.add_argument('--out_path', type=str, default='./', help='output path')
    parser.add_argument('--xml_path', type=str, default='./', help='xml path')
    parser.add_argument('--name', type=str, default='./Supercharge', help='job name')
    parser.add_argument('--node', type=int, default=8, help='num of nodes')
    parser.add_argument('--ntasks', type=int, default=16, help='ntasks per node')
    parser.add_argument('--ref_path', type=str, default='./ref.txt', help='ref path')
    parser.add_argument('--num', type=int, default=5000, help='nstruct')

    args = parser.parse_args()
    
    max_len = args.end_pos - args.start_pos + 1 
    pos_lst = get_mutant_pos(args.wt_path, args.super_path, args.chain)

    # neigh = neighbor(args.super_path, pos_lst, args.distance, max_len, args.chain)
    neigh = ",".join(pos_lst)
    gene_compm(args.shell_path, args.name, args.node, args.ntasks, args.super_path, args.wt_path, args.out_path, args.xml_path, args.ref_path, args.num, neigh, args.chain)
    
