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
TARGET_METHOD = config['TARGET_METHOD']
TARGET_CHARGE = config['TARGET_CHARGE']


rule all:
    input:
        DATA_PATH +'/Supercharge' + '/success.log',
        DATA_PATH +'/Supercharge/' + WT_NAME + '_Mutated.pdb',
        DATA_PATH +'/Supercharge/' + 'resfile_output_Rsc.txt',
        RUN_FILE + '/Supercharge_ref.sh',
        RUN_FILE + '/Superref_success.log'

rule SUPERCHARGE:
    input:
        Relaxed_path = DATA_PATH + '/Relaxed_WT/' + WT_NAME + '_Relaxed.pdb'
    output:
        DATA_PATH +'/Supercharge' + '/success.log'
    params:
        Flags_path = UTILS_PATH + '/Supercharge/' + TARGET_CHARGE +'_'+ TARGET_METHOD + '.flags',
        Out_path = DATA_PATH +'/Supercharge/'
    threads:
        1
    shell:
        """
        {ROSETTA_BIN}/supercharge.default.linuxgccrelease\
        -in:file:s {input.Relaxed_path}\
        -out:path {params.Out_path}\
        @ {params.Flags_path} && touch {output}
        """

rule MOVE_SUPERCHARGE:
    input:
        DATA_PATH +'/Supercharge' + '/success.log'
    output:
        Pdb = DATA_PATH +'/Supercharge/' + WT_NAME + '_Mutated.pdb',
        Ref = DATA_PATH +'/Supercharge/' + 'resfile_output_Rsc.txt'
    params:
        Scripts_path = UTILS_PATH + '/Supercharge/move.py',
        Out_path = DATA_PATH +'/Supercharge/',
        Wt_name = WT_NAME,
        Python_path = PYTHON_PATH
    threads:
        1
    shell:
        """
        {params.Python_path} {params.Scripts_path}\
         --input_path {params.Out_path}\
         --wt_name {params.Wt_name}\
         --output_pdb {output.Pdb}\
         --output_ref {output.Ref}
        """      

rule gen_Com_PM:
    input:
        Supercharge_report = DATA_PATH +'/Supercharge/' + 'resfile_output_Rsc.txt'
    output:
        Shell_file = RUN_FILE + '/Supercharge_ref.sh'
    params:
        Distance_py =  UTILS_PATH + '/MC/distance_Supercharge_ref.py',
        WT_path = DATA_PATH + '/Cleaned_WT/' + WT_NAME + '_' + TARGET_CHAIN + '.pdb',
        Distance = DISTANCE,
        Chain = TARGET_CHAIN,
        Start_pos = PDB_START,
        End_pos = PDB_END,
        Relax_path = DATA_PATH + '/Relaxed_WT/' + WT_NAME + '_Relaxed.pdb',
        Out_path = DATA_PATH + '/Com_SuperREF',
        Scripts_path = UTILS_PATH + '/MC/ComboPM_with.xml',
        Name = WORK_NAME,
        Node = NODE,
        Ntasks = NTASKS,
        Ref_path = RUN_FILE + '/ref.txt',
        Num = NUM,
        Python_path = PYTHON_PATH
    shell:
        """
        {params.Python_path} {params.Distance_py}\
         --wt_path {params.WT_path}\
         --super_ref_path {input.Supercharge_report}\
         --distance {params.Distance}\
         --chain {params.Chain}\
         --start_pos {params.Start_pos}\
         --end_pos {params.End_pos}\
         --shell_path {output.Shell_file}\
         --input_path {params.Relax_path}\
         --out_path {params.Out_path}\
         --xml_path {params.Scripts_path}\
         --name {params.Name}\
         --node {params.Node}\
         --ntasks {params.Ntasks}\
         --ref_path {params.Ref_path}\
         --num {params.Num}
        """


rule Com_PM:
    input:
        RUN_FILE + '/Supercharge_ref.sh'
    output:
        RUN_FILE + '/Superref_success.log'
    params:
        CM_PATH = DATA_PATH + '/Com_SuperREF',
        success_log = OUTPUT_DIR + 'success.log'
    threads:
        THREADS
    shell:
        """
        mkdir -p {params.CM_PATH}
        sh {input} && touch {output} && touch {params.success_log}
        """
