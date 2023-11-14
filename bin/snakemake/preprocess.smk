configfile: 'config.yaml'

## Required paths
ROSETTA = config['ROSETTA']
ROSETTA_BIN = config['ROSETTA_BIN']
WORK_NAME = config['WORK_NAME']
WT_NAME = config['WT_NAME']

WORK_DIR = config['WORK_DIR']
INPUT_DIR = config['INPUT_DIR']
OUTPUT_DIR = config['OUTPUT_DIR']

UTILS_PATH = config['UTILS_PATH']
DATA_PATH = config['DATA_PATH']
RUN_FILE = config['RUN_FILE']
PYTHON_PATH = config['PYTHON_PATH']

## Default params
ALL_CHAINS = config['ALL_CHAINS']
TARGET_CHAIN = config['TARGET_CHAIN']
ANOTHER_CHAIN = config['ANOTHER_CHAIN']
DISTANCE = config['DISTANCE']
PDB_START = config['PDB_START']
PDB_END = config['PDB_END']
THREADS = config['THREADS']
NODE = config['NODE']
NTASKS = config['NTASKS']
NUM = config['NUM']

## LIST
AA_LST  = ['ALA', 'CYS', 'ASP', 'GLU', 'PHE', 'GLY', 'HIS', 'ILE', 'LYS', 'LEU', 'MET', 'ASN', 'PRO', 'GLN', 'ARG', 'SER', 'THR', 'VAL', 'TRP', 'TYR']
POS_LST = [str(i+1) for i in range((PDB_END - PDB_START + 1))]


## main
rule all:
    input:
        DATA_PATH + '/WT/' + WT_NAME + '.pdb',
        DATA_PATH + '/Cleaned_WT/' + WT_NAME + '_' + TARGET_CHAIN + '.pdb',
        DATA_PATH + '/Cleaned_WT/' + WT_NAME + '_' + TARGET_CHAIN + '.fasta',
        DATA_PATH + '/Relaxed_WT/score_Relaxed.sc',
        DATA_PATH + '/Relaxed_WT/' + WT_NAME + '_Relaxed.pdb',
        expand(DATA_PATH + '/PM/{pos}/{aa}/success.log', pos=POS_LST, aa=AA_LST),
        RUN_FILE + '/ref.txt',
        RUN_FILE + '/d_score.csv',
        RUN_FILE + '/all.txt'


rule Clean_WT:
    input:
        WT = WORK_DIR + '/data' + '/' + WT_NAME + '.pdb'
    output:
        New_WT = DATA_PATH + '/WT/' + WT_NAME + '.pdb',
        Cleaned = DATA_PATH + '/Cleaned_WT/' + WT_NAME + '_' + TARGET_CHAIN + '.pdb',
        Out_TARGET_fa = DATA_PATH + '/Cleaned_WT/' + WT_NAME + '_' + TARGET_CHAIN + '.fasta',
    params:
        Process = UTILS_PATH + '/PM/process.py',
        PDB_out = WT_NAME + '_' + TARGET_CHAIN + '.pdb',
        TARGET_fa = WT_NAME + '_' + TARGET_CHAIN + '.fasta',
        Python_path = PYTHON_PATH,
        Chain = TARGET_CHAIN
    threads:
        1
    shell:
        """
        {params.Python_path} {params.Process} --wt_path {input.WT} --out_path {output.New_WT} --chain {params.Chain} && \
        {params.Python_path} {ROSETTA}/main/tools/protein_tools/scripts/clean_pdb.py {output.New_WT} {params.Chain} && \
        mv {params.TARGET_fa} {output.Out_TARGET_fa} && \
        mv {params.PDB_out} {output.Cleaned}
        """

rule Relax_cleaned:
    input:
        Cleaned = DATA_PATH + '/Cleaned_WT/' + WT_NAME + '_' + TARGET_CHAIN + '.pdb'
    output:
        Relaxed = DATA_PATH + '/Relaxed_WT/score_Relaxed.sc',
        New_name = DATA_PATH + '/Relaxed_WT/' + WT_NAME + '_Relaxed.pdb'
    params:
        Out_path = DATA_PATH + '/Relaxed_WT/',
        Flags_path = UTILS_PATH + '/relax/relax.flags',
        Out_name = DATA_PATH + '/Relaxed_WT/' + WT_NAME + '_' + TARGET_CHAIN + '_Relaxed_0001.pdb'
    threads:
        1
    shell:
        """
        {ROSETTA_BIN}/relax.linuxgccrelease -in:file:s {input.Cleaned}\
         -out:path:pdb {params.Out_path}\
         -out:path:score {params.Out_path}\
         -suffix '_Relaxed'\
         @ {params.Flags_path} && mv {params.Out_name} {output.New_name}
        """

rule PM:
    input:
        Relaxed = DATA_PATH + '/Relaxed_WT/' + WT_NAME + '_Relaxed.pdb'
    output:
        DATA_PATH + '/PM/{pos}/{aa}/success.log'
    params:
        Protocol = UTILS_PATH + '/PM/PM_ssm_protocol.xml',
        Output_dir = DATA_PATH + '/PM/{pos}/{aa}',
        Pos = "{pos}",
        AA = "{aa}"
    threads:
        1
    shell:
        """
        {ROSETTA_BIN}/rosetta_scripts.linuxgccrelease\
         -in:file:s {input.Relaxed}\
         -parser:protocol {params.Protocol}\
         -nstruct 5\
         -out:path:pdb {params.Output_dir}\
         -out:path:score {params.Output_dir}\
         -parser:script_vars\
         pos={params.Pos}\
         aa={params.AA} && touch {output}
        """# touch for check

rule gen_ref:
    input:
        expand(DATA_PATH + '/PM/{pos}/{aa}/success.log', pos=POS_LST, aa=AA_LST)
    output:
        Ref_path = RUN_FILE + '/ref.txt',
        Socre_path = RUN_FILE + '/d_score.csv',
        All_path = RUN_FILE + '/all.txt'
    params:
        Python_file = UTILS_PATH + '/PM/analys_score.py',
        Cleaned_fasta = DATA_PATH + '/Cleaned_WT/' + WT_NAME + '_' + TARGET_CHAIN + '.fasta',
        In_path = DATA_PATH + '/PM',
        Out_path = RUN_FILE,
        End_Pos = PDB_END - PDB_START + 1,
        Chain = TARGET_CHAIN,
        Python_path = PYTHON_PATH
    threads:
        1
    shell:
        """
        {params.Python_path} {params.Python_file}\
         --input_path {params.In_path}\
         --output_path {params.Out_path}\
         --start_pos 1\
         --end_pos {params.End_Pos}\
         --target_fasta {params.Cleaned_fasta}\
         --chain {params.Chain}
        """
