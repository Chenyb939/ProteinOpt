import os
import yaml
import shutil
import argparse
import warnings
from Bio.PDB import PDBParser
warnings.filterwarnings("ignore")

def preparation(BIN_DIR, WORK_DIR, WORK_NAME, INPUT_FILE):
    if not os.path.exists(WORK_DIR):
        os.mkdir(WORK_DIR)
    if not os.path.exists(os.path.join(WORK_DIR, WORK_NAME)):
        os.mkdir(os.path.join(WORK_DIR, WORK_NAME))

    os.mkdir(os.path.join(WORK_DIR, WORK_NAME, 'data'))

    shutil.copytree(os.path.join(BIN_DIR, 'snakemake'), os.path.join(WORK_DIR, WORK_NAME, 'snakemake'))
    shutil.copytree(os.path.join(BIN_DIR, 'utils'), os.path.join(WORK_DIR, WORK_NAME, 'utils'))
    shutil.move(INPUT_FILE, os.path.join(WORK_DIR, WORK_NAME, 'data'))
    # shutil.copy(INPUT_FILE, os.path.join(WORK_DIR, WORK_NAME, 'data'))

def read_pdb_para(input_file, target_chain):
    p = PDBParser()
    name = os.path.basename(input_file)[:-4]
    structure = p.get_structure(name, input_file)
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

    target_pos = all_pos[all_chains.index(target_chain.upper())]
    target_pos_num = [x for x in target_pos if x.isdigit()]
    target_pos_num_sort = sorted(map(int, target_pos_num))
    start_pos = target_pos_num_sort[0]
    end_pos = target_pos_num_sort[-1]
    other_chain = all_chains.replace(target_chain, '')

    pdb_len = 0
    for i in all_pos:
        pdb_len += len(i)
    return name, all_chains, other_chain, int(start_pos), int(end_pos), pdb_len

def write_config(WORK_NAME, WT_NAME, WORK_DIR, ALL_CHAINS, TARGET_CHAIN, ANOTHER_CHAIN, DISTANCE, PDB_START, PDB_END, NODE, NTASKS, NUM, PDB_TOTAL, TARGET_METHOD, TARGET_CHARGE, TOP_PM_NUM, IN_SITE, Rosetta):
    WORK_DIR = os.path.join(WORK_DIR, WORK_NAME)
    INPUT_DIR = os.path.join(WORK_DIR, 'data')
    OUTPUT_DIR = os.path.join(WORK_DIR, 'output')
    UTILS_PATH = os.path.join(WORK_DIR, 'utils')
    DATA_PATH = os.path.join(OUTPUT_DIR, 'data')
    RUN_FILE = os.path.join(OUTPUT_DIR, 'utils')
    Rosetta_bin = os.path.join(Rosetta, 'bin')
    PYTHON_PATH = os.popen('which python').readlines()[0].replace('\n', '')
    RUN_DIR = os.popen('pwd').readlines()[0].replace('\n', '')
    THREADS = NODE * NTASKS
    names = {
    'ROSETTA': Rosetta,
    'ROSETTA_BIN': Rosetta_bin,
    'WORK_NAME': WORK_NAME,
    'WT_NAME': WT_NAME,
    'WORK_DIR': WORK_DIR,
    'INPUT_DIR': INPUT_DIR,
    'OUTPUT_DIR': OUTPUT_DIR,
    'RUN_DIR': RUN_DIR,
    'UTILS_PATH': UTILS_PATH,
    'DATA_PATH': DATA_PATH,
    'RUN_FILE': RUN_FILE,
    'PYTHON_PATH': PYTHON_PATH,
    'ALL_CHAINS': ALL_CHAINS,
    'TARGET_CHAIN': TARGET_CHAIN,
    'ANOTHER_CHAIN':ANOTHER_CHAIN,
    'DISTANCE': DISTANCE,
    'PDB_START': PDB_START,
    'PDB_END': PDB_END,
    'THREADS': THREADS,
    'NODE': NODE,
    'NTASKS': NTASKS,
    'NUM': NUM,
    'PM_NUM': 1,
    'PDB_TOTAL': PDB_TOTAL,
    'TARGET_METHOD': TARGET_METHOD,
    'TARGET_CHARGE': TARGET_CHARGE,
    'TOP_PM_NUM': TOP_PM_NUM,
    'IN_SITE': IN_SITE
    }
    with open(os.path.join(WORK_DIR, 'snakemake', 'config.yaml'), 'w') as file:
         yaml.dump(names, file, sort_keys=False)

def write_bash(WORK_DIR, job_name, node, ntasks):
    SNAKE_dir = os.path.join(WORK_DIR, job_name, 'snakemake', '')
    with open(os.path.join(WORK_DIR, job_name, 'snakemake', 'preprocess.sh'), 'w') as file:
        file.write(f'#!/bin/bash\n#SBATCH --output {job_name}%j.out\n#SBATCH --job-name {job_name}_preprocess\n#SBATCH --nodes={node}\n#SBATCH --ntasks-per-node={ntasks}\n\nsnakemake -s {SNAKE_dir}preprocess.smk -j {node*ntasks}')
    with open(os.path.join(WORK_DIR, job_name,'snakemake', 'PMS.sh'), 'w') as file:
        file.write(f'#!/bin/bash\n#SBATCH --output {job_name}%j.out\n#SBATCH --job-name {job_name}_PMS\n#SBATCH --nodes={node}\n#SBATCH --ntasks-per-node={ntasks}\n\nsnakemake -s {SNAKE_dir}PMS.smk -j {node*ntasks}')
    with open(os.path.join(WORK_DIR, job_name,'snakemake', 'Supercharge.sh'), 'w') as file:
        file.write(f'#!/bin/bash\n#SBATCH --output {job_name}%j.out\n#SBATCH --job-name {job_name}_Supercharge\n#SBATCH --nodes={node}\n#SBATCH --ntasks-per-node={ntasks}\n\nsnakemake -s {SNAKE_dir}Supercharge.smk -j {node*ntasks}')
    with open(os.path.join(WORK_DIR, job_name,'snakemake', 'Supercharge_ref.sh'), 'w') as file:
        file.write(f'#!/bin/bash\n#SBATCH --output {job_name}%j.out\n#SBATCH --job-name {job_name}_Supercharge_ref\n#SBATCH --nodes={node}\n#SBATCH --ntasks-per-node={ntasks}\n\nsnakemake -s {SNAKE_dir}Supercharge_ref.smk -j {node*ntasks}')
    with open(os.path.join(WORK_DIR, job_name,'snakemake', 'RosettaVIP.sh'), 'w') as file:
        file.write(f'#!/bin/bash\n#SBATCH --output {job_name}%j.out\n#SBATCH --job-name {job_name}_RosettaVIP\n#SBATCH --nodes={node}\n#SBATCH --ntasks-per-node={ntasks}\n\nsnakemake -s {SNAKE_dir}RosettaVIP.smk -j {node*ntasks}')
    with open(os.path.join(WORK_DIR, job_name,'snakemake', 'Manual.sh'), 'w') as file:
        file.write(f'#!/bin/bash\n#SBATCH --output {job_name}%j.out\n#SBATCH --job-name {job_name}_Manual\n#SBATCH --nodes={node}\n#SBATCH --ntasks-per-node={ntasks}\n\nsnakemake -s {SNAKE_dir}Manual.smk -j {node*ntasks}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--job_name', type=str, help='job name')
    parser.add_argument('--input_file', type=str, help='PDB file to design')
    parser.add_argument('--target_chain', type=str, help='chain to design')
    parser.add_argument('--distance', type=int, default=7, help='distance around site')
    parser.add_argument('--node', type=int, default=1, help='nodes use in HPC')
    parser.add_argument('--ntasks', type=int, default=8, help='ntasks use in each node')
    parser.add_argument('--num', type=int, default=10, help='number of generated PDBs')
    parser.add_argument('--super_method', type=str, default='residue', help='supercharge methods if use')  
    parser.add_argument('--super_target', type=str, default='positive', help='supercharge target if use')
    parser.add_argument('--top_pm_num', type=int, default=10, help='number of point mutation selected')
    parser.add_argument('--in_site', type=str, default='1F,52I', help='location of mutation point, such as "1F,52I"')
    parser.add_argument('--Rosetta_dir', type=str, help='Path to the ROSETTA software')
    parser.add_argument('--output_dir', type=str, default='./', help='Output File Directory')
    parser.add_argument('--proteinopt_bin', type=str, default='./', help='The bin directory of ProteinOpt')
    args = parser.parse_args()

    assert args.super_method in ['atom', 'residue'] , 'super_method should be atom or residue'
    assert args.super_target in ['positive', 'negative'] , 'super_method should be positive or negative'

    # WORK_DIR = str(os.getcwd())
    # BIN_DIR = str(os.path.join(WORK_DIR, 'bin'))

    WORK_DIR = args.output_dir
    BIN_DIR = args.proteinopt_bin

    preparation(BIN_DIR, WORK_DIR, args.job_name, args.input_file)
    wt_name, all_chains, other_chain, start_pos, end_pos, pdb_total = read_pdb_para(os.path.join(WORK_DIR, args.job_name, 'data', os.path.basename(args.input_file)), args.target_chain)
    write_config(args.job_name, wt_name, WORK_DIR, all_chains, args.target_chain, other_chain,args.distance, start_pos, end_pos, args.node, args.ntasks, args.num, pdb_total, args.super_method, args.super_target, args.top_pm_num, args.in_site, args.Rosetta_dir)
    write_bash(WORK_DIR, args.job_name, args.node, args.ntasks)
    # order
    # python stab_dp.py --job_name 6m0j --input_file /share/home/cheny/Projects/stable_final/test/data/6m0j.pdb --target_chain E --distance 7 --num 100 --in_site 498R