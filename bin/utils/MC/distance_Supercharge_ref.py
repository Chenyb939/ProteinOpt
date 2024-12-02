import os
import argparse
import copy
from pyrosetta import pose_from_pdb, init
from pyrosetta.rosetta.core.select.residue_selector import NeighborhoodResidueSelector, ResidueIndexSelector
import warnings

warnings.filterwarnings('ignore')

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


def get_mutant_pos(path, chain):
    pos_lst = []
    aa_lst = []
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith(' ') and line[3:].replace('\n', '').split(' ')[1] == chain:
                if '#' in line:
                    pass
                else:
                    line = line[3:].replace('\n', '').split(' ')
                    pos_lst.append(line[0])
                    aa_lst.append(line[-1])
    ref_pos_lst = copy.deepcopy(pos_lst)
    pos_lst.sort(reverse=False)
    pos_lst = [str(i) + chain for i in pos_lst]
    return pos_lst, ref_pos_lst, aa_lst


def gene_compm(shell_path, name, node, ntasks, input_path, wt_path, out_path, xml_path, ref_path, num, neig, chain):
    ref_path = ref_path.replace('.txt', '_new.txt')
    with open(os.path.join(shell_path), 'w') as file:
        # file.write(f'#!/bin/bash\n#SBATCH --output {name}%j.out\n#SBATCH --job-name {name}\n#SBATCH --nodes={node}\n#SBATCH --ntasks-per-node={ntasks}\n')
        file.write(f'mpirun -n {node*ntasks} $ROSETTA_BIN/rosetta_scripts.mpi.linuxgccrelease -s {input_path} -in:file:native {wt_path} -out:path:pdb {out_path} -out:path:score {out_path} -linmem_ig 10 -nstruct {num} -parser:protocol {xml_path} -parser:script_vars resfile={ref_path} multichain={chain} multiposition={neig} bonusvalue=2.25')


def write_new_ref(inpath, pos_lst, aa_lst, chain):
    pos_lst_o = []
    aa_lst_o = []
    with open(inpath, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line[0].isdigit() == True:
                pos_lst_o.append(line.split(' ')[0])
                aa_lst_o.append(line.replace('\n', '').split(' ')[-1])
    pos_lst_n = []
    aa_lst_n = []
    for index in range(len(pos_lst_o)):
        if pos_lst_o[index] in pos_lst:
            pos = pos_lst_o[index]
            aa = aa_lst_o[index] + aa_lst[pos_lst.index(pos_lst_o[index])]
            aa = ''.join(sorted(set(list(aa))))
            pos_lst_n.append(pos)
            aa_lst_n.append(aa)
        else:
            pos_lst_n.append(pos_lst_o[index])
            aa_lst_n.append(aa_lst_o[index])
    other_lst = [item for item in pos_lst if not item in pos_lst_o]

    for index in other_lst:
        pos = index
        aa = aa_lst[pos_lst.index(index)]
        pos_lst_n.append(pos)
        aa_lst_n.append(aa)
    fin_pos_lst = copy.deepcopy(pos_lst_n)
    fin_pos_lst = [int(i) for i in fin_pos_lst]
    fin_pos_lst.sort(reverse=False)
    fin_pos_lst = [str(i) for i in fin_pos_lst]
    fin_aa_lst = []
    for i in fin_pos_lst:
        fin_aa_lst.append(aa_lst_n[pos_lst_n.index(i)])
        
    with open(inpath.replace('.txt', '_new.txt'), 'w') as file:
        file.write('NATAA\nUSE_INPUT_SC\n\nStart\n\n')
        for i in range(len(fin_pos_lst)):
            file.write(f'{fin_pos_lst[i]} {chain} PIKAA {fin_aa_lst[i]}\n')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Generate xml file for mutation')
    parser.add_argument('--wt_path', type=str, default='./6yz5.pdb', help='WT pdb file')
    parser.add_argument('--super_ref_path', type=str, help='Supercharge ref path')
    parser.add_argument('--distance', type=float, default=7.0, help='The distance around target amino acids')
    parser.add_argument('--chain', type=str, default='E', help='chain to design')
    parser.add_argument('--start_pos', type=int, default=334, help='The first residue position of the chain to be designed in the pdb file')
    parser.add_argument('--end_pos', type=int, default=528, help='The last residue position of the chain to be designed in the pdb file')
    parser.add_argument('--shell_path', type=str, default='./', help='shell path')
    parser.add_argument('--input_path', type=str, default='./', help='input path')
    parser.add_argument('--out_path', type=str, default='./', help='output path')
    parser.add_argument('--xml_path', type=str, default='./', help='xml path')
    parser.add_argument('--name', type=str, default='./VIP', help='job name')
    parser.add_argument('--node', type=int, default=8, help='num of nodes')
    parser.add_argument('--ntasks', type=int, default=16, help='ntasks per node')
    parser.add_argument('--ref_path', type=str, help='ref path')
    parser.add_argument('--num', type=int, default=5000, help='nstruct')

    args = parser.parse_args()
    
    max_len = args.end_pos - args.start_pos + 1 
    pos_lst, ref_pos_lst, aa_lst= get_mutant_pos(args.super_ref_path, args.chain)
    write_new_ref(args.ref_path, ref_pos_lst, aa_lst, args.chain)

    # neigh = neighbor(args.input_path, pos_lst, args.distance, max_len, args.chain)
    neigh = ",".join(pos_lst)
    gene_compm(args.shell_path, args.name, args.node, args.ntasks, args.input_path, args.wt_path, args.out_path, args.xml_path, args.ref_path, args.num, neigh, args.chain)
