import os
import argparse
from Bio.PDB import PDBParser
import warnings

warnings.filterwarnings('ignore')

def get_mutant_pos_new(out_path, pdb_path, target_chain):
    p=PDBParser()
    p_name = os.path.splitext(pdb_path)[0].split('/')[-1]
    structure =p.get_structure(p_name, pdb_path)
    all_chains = ''
    all_pos = []
    for model in structure:
        for chain in model:
            a = str(chain)
            a = a.split('=')[-1].replace('>', '')
            all_chains += str(a)
            chain_pos = []
            for residue in chain:
                    b = str(residue)
                    b = b.split(' ')[4].split('=')[-1]
                    if b == '':
                        break
                    else:
                        chain_pos.append(b)
            all_pos.append(chain_pos)

    with open(out_path, 'w') as file:
        num = 0
        for i in range(len(all_chains)):
            if i != all_chains.index(target_chain.upper()):
                for b in all_pos[i]:
                    num += 1
                    file.write('{} {}\n'.format(num, str(chain).split('=')[-1].replace('>', '')))
                    # print('{} {}\n'.format(num, str(chain).split('=')[-1].replace('>', '')))
            else:
                for b in all_pos[i]:
                    num += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Generate ref file for VIP')
    parser.add_argument('--out_path', type=str, default='./Chain.txt', help='out path')
    parser.add_argument('--pdb_path', type=str, default='./', help='PDB file to be designed')
    parser.add_argument('--target_chain', type=str, default='E', help='Chain to be designed')

    args = parser.parse_args()
    get_mutant_pos_new(args.out_path, args.pdb_path, args.target_chain)