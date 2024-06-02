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
TOP_PM_NUM = config['TOP_PM_NUM']


## main
rule all:
    input:
        RUN_FILE + '/PMS.sh',
        DATA_PATH + '/Com_PM_PM/socre.sc'


rule gen_Com_PM:
    input:
        D_score = RUN_FILE + '/d_score.csv'
    output:
        Shell_file = RUN_FILE + '/PMS.sh'
    params:
        Distance_py =  UTILS_PATH + '/MC/distance_PM.py',
        WT_path = DATA_PATH + '/Cleaned_WT/' + WT_NAME + '_' + TARGET_CHAIN + '.pdb',
        Final_Relaxed = DATA_PATH + '/Relaxed_WT/' + WT_NAME + '_Relaxed.pdb',
        Scripts_path = UTILS_PATH + '/MC/ComboPM_with.xml',
        Ref_path = RUN_FILE + '/ref.txt',
        Top_num = TOP_PM_NUM,
        Distance = DISTANCE,
        Chain = TARGET_CHAIN,
        Start_pos = PDB_START,
        End_pos = PDB_END,
        Out_path = DATA_PATH + '/Com_PM_PM',
        Name = WORK_NAME,
        Node = NODE,
        Ntasks = NTASKS,
        Num = NUM,
        Python_path = PYTHON_PATH
    shell:
        """
        {params.Python_path} {params.Distance_py}\
         --wt_path {params.WT_path}\
         --d_score {input.D_score}\
         --top_num {params.Top_num}\
         --distance {params.Distance}\
         --chain {params.Chain}\
         --start_pos {params.Start_pos}\
         --end_pos {params.End_pos}\
         --shell_path {output.Shell_file}\
         --input_path {params.Final_Relaxed}\
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
        RUN_FILE + '/PMS.sh'
    output:
        DATA_PATH + '/Com_PM_PM/socre.sc'
    params:
        DATA_PATH + '/Com_PM_PM'
    threads:
        THREADS
    shell:
        """
        mkdir -p {params} && sh {input}   
        """
