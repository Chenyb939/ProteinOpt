configfile: 'config.yaml'

## Required paths
ROSETTA = config['ROSETTA']
ROSETTA_BIN = config['ROSETTA_BIN']
WORK_NAME = config['WORK_NAME']
WT_NAME = config['WT_NAME']

WORK_DIR = config['WORK_DIR']
INPUT_DIR = config['INPUT_DIR']
OUTPUT_DIR = config['OUTPUT_DIR']
RUN_DIR = config['RUN_DIR']

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
PDB_TOTAL = config['PDB_TOTAL']

## main
rule all:
    input:
        RUN_FILE + '/Chain.txt',
        RUN_FILE + '/VIP_success.marker',
        RUN_FILE + '/reports.txt',
        RUN_FILE + '/mutate.xml',
        DATA_PATH + '/VIPMutate/score_Mutated.sc',  
        DATA_PATH + '/VIPMutate/' + WT_NAME + '_Mutated.pdb',
        DATA_PATH + '/VIPMutated_Relaxed/score_Relaxed.sc',
        DATA_PATH + '/VIPMutated_Relaxed/' + WT_NAME + '_final_Relaxed.pdb',
        RUN_FILE + '/RosettaVIP.sh',
        RUN_FILE + '/VIP_success.log'


rule gen_VIP_ref:
    input:
        ref_py = UTILS_PATH + '/VIP/get_VIP_ref.py',
    output:
        RUN_FILE + '/Chain.txt'
    params:
        Chain = TARGET_CHAIN,
        Relaxed_path = DATA_PATH + '/Relaxed_WT/' + WT_NAME + '_Relaxed.pdb',
        Python_path = PYTHON_PATH
    shell:
        """
        {params.Python_path} {input.ref_py}\
         --out_path {output}\
         --pdb_path {params.Relaxed_path}\
         --target_chain {params.Chain}
        """

rule VIP:
    input:
        exclude_path = RUN_FILE + '/Chain.txt'
    output:
        RUN_FILE + '/VIP_success.marker'
    params:
        Out_path = DATA_PATH + '/VIPMutate',
        Relaxed_path = DATA_PATH + '/Relaxed_WT/' + WT_NAME + '_Relaxed.pdb',
        Flags_path = UTILS_PATH + '/VIP/VIP.flags',
        Log_path = RUN_FILE + '/VIP_failed.log'
    threads:
        1
    shell:
        """
        {ROSETTA_BIN}/vip.linuxgccrelease\
        -in:file:s {params.Relaxed_path}\
        -cp:exclude_file {input.exclude_path}\
        -out:path:all {params.Out_path}
        @ {params.Flags_path} && touch {output} || touch {params.Log_path}
        """

rule move_VIP:
    input:
        RUN_FILE + '/VIP_success.marker'
    output:
        reports = RUN_FILE + '/reports.txt'
    params:
        reports = RUN_DIR + '/reports.txt',
    threads:
        1
    shell:
        """
        mv {params.reports} {output.reports}
        """

rule gen_Mutate:
    input:
        reports = RUN_FILE + '/reports.txt'
    output:
        xml_path = RUN_FILE + '/mutate.xml'
    params:
        mut_xml_py = UTILS_PATH + '/mutate/get_mut_xml_VIP.py',
        Chain = TARGET_CHAIN,
        Python_path = PYTHON_PATH
    shell:
        """
        {params.Python_path} {params.mut_xml_py}\
         --input_file {input.reports}\
         --output_file {output.xml_path}\
         --chain {params.Chain}
        """

rule Mutate_relaxed:
    input:
        Scrpits_path = RUN_FILE + '/mutate.xml'
    output:
        Relaxed = DATA_PATH + '/VIPMutate/score_Mutated.sc',
        New_name = DATA_PATH + '/VIPMutate/' + WT_NAME + '_Mutated.pdb'
    params:
        Relaxed_path = DATA_PATH + '/Relaxed_WT/' + WT_NAME + '_Relaxed.pdb',
        WT_path = DATA_PATH + '/Cleaned_WT/' + WT_NAME + '_' + TARGET_CHAIN + '.pdb',
        Out_path = DATA_PATH + '/VIPMutate/',
        Out_name = DATA_PATH + '/VIPMutate/' + WT_NAME + '_Relaxed_Mutated_0001.pdb'
    threads:
        1
    shell:
        """
        {ROSETTA_BIN}/rosetta_scripts.linuxgccrelease\
         -in:file:s {params.Relaxed_path}\
         -in:file:native {params.WT_path}\
         -parser:protocol {input.Scrpits_path}\
         -linmem_ig 10\
         -nstruct 1\
         -suffix '_Mutated'\
         -out:overwrite\
         -out:path:pdb {params.Out_path}\
         -out:path:score {params.Out_path} && mv {params.Out_name} {output.New_name}
        """

rule Relax_Mutated:
    input:
        Mutated_name = DATA_PATH + '/VIPMutate/' + WT_NAME + '_Mutated.pdb'
    output:
        Relaxed = DATA_PATH + '/VIPMutated_Relaxed/score_Relaxed.sc',
        New_name = DATA_PATH + '/VIPMutated_Relaxed/' + WT_NAME + '_final_Relaxed.pdb'
    params:
        Flags_path = UTILS_PATH + '/relax/relax.flags',
        Out_path = DATA_PATH + '/VIPMutated_Relaxed/',
        Out_name = DATA_PATH + '/VIPMutated_Relaxed/' + WT_NAME + '_Mutated_Relaxed_0001.pdb'
    threads:
        1
    shell:
        """
        {ROSETTA_BIN}/relax.linuxgccrelease -in:file:s {input.Mutated_name}\
         -out:path:pdb {params.Out_path}\
         -out:path:score {params.Out_path}\
         -suffix '_Relaxed'\
         @ {params.Flags_path} && mv {params.Out_name} {output.New_name}
        """

rule gen_Com_PM:
    input:
        Final_Relaxed = DATA_PATH + '/VIPMutated_Relaxed/' + WT_NAME + '_final_Relaxed.pdb'
    output:
        Shell_file = RUN_FILE + '/RosettaVIP.sh'
    params:
        Distance_py =  UTILS_PATH + '/MC/distance_VIP.py',
        Vip_report = RUN_FILE + '/reports.txt',
        WT_path = DATA_PATH + '/Cleaned_WT/' + WT_NAME + '_' + TARGET_CHAIN + '.pdb',
        Distance = DISTANCE,
        Chain = TARGET_CHAIN,
        Start_pos = PDB_START,
        End_pos = PDB_END,
        Out_path = DATA_PATH + '/Com_VIP',
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
         --vip_result {params.Vip_report}\
         --distance {params.Distance}\
         --chain {params.Chain}\
         --start_pos {params.Start_pos}\
         --end_pos {params.End_pos}\
         --shell_path {output.Shell_file}\
         --input_path {input.Final_Relaxed}\
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
        RUN_FILE + '/RosettaVIP.sh'
    output:
        RUN_FILE + '/VIP_success.log'
    params:
        CM_PATH = DATA_PATH + '/Com_VIP',
        success_log = OUTPUT_DIR + 'success.log'
    threads:
        THREADS
    shell:
        """
        mkdir -p {params.CM_PATH}
        sh {input} && touch {output} && touch {params.success_log}
        """
