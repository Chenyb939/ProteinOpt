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
IN_SITE = config['IN_SITE']


## main
rule all:
    input:
        RUN_FILE + '/mutate.xml',
        DATA_PATH + '/Mutate/score_Mutated.sc',  
        DATA_PATH + '/Mutate/' + WT_NAME + '_Mutated.pdb',
        DATA_PATH + '/Mutated_Relaxed/score_Relaxed.sc',
        DATA_PATH + '/Mutated_Relaxed/' + WT_NAME + '_final_Relaxed.pdb',
        RUN_FILE + '/Manual.sh',
        DATA_PATH + '/Com_PM_DMS/socre.sc'
    

rule gen_Mutate:
    input:
        mut_xml_py = UTILS_PATH + '/mutate/get_mut_xml_DMS.py'
    output:
        xml_path = RUN_FILE + '/mutate.xml'
    params:
        In_site = IN_SITE,
        Chain = TARGET_CHAIN,
        Start_pos = PDB_START,
        Python_path = PYTHON_PATH
    shell:
        """
        {params.Python_path} {input.mut_xml_py}\
         --in_site {params.In_site}\
         --output_file {output.xml_path}\
         --chain {params.Chain}\
         --start_pos {params.Start_pos}
        """

rule Mutate_relaxed:
    input:
        Scrpits_path = RUN_FILE + '/mutate.xml'
    output:
        Relaxed = DATA_PATH + '/Mutate/score_Mutated.sc',
        New_name = DATA_PATH + '/Mutate/' + WT_NAME + '_Mutated.pdb'
    params:
        Relaxed_path = DATA_PATH + '/Relaxed_WT/' + WT_NAME + '_Relaxed.pdb',
        WT_path = DATA_PATH + '/Cleaned_WT/' + WT_NAME + '_' + TARGET_CHAIN + '.pdb',
        Out_path = DATA_PATH + '/Mutate/',
        Out_name = DATA_PATH + '/Mutate/' + WT_NAME + '_Relaxed_Mutated_0001.pdb'
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
        Mutated_name = DATA_PATH + '/Mutate/' + WT_NAME + '_Mutated.pdb'
    output:
        Relaxed = DATA_PATH + '/Mutated_Relaxed/score_Relaxed.sc',
        New_name = DATA_PATH + '/Mutated_Relaxed/' + WT_NAME + '_final_Relaxed.pdb'
    params:
        Flags_path = UTILS_PATH + '/relax/relax.flags',
        Out_path = DATA_PATH + '/Mutated_Relaxed/',
        Out_name = DATA_PATH + '/Mutated_Relaxed/' + WT_NAME + '_Mutated_Relaxed_0001.pdb'
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
        Final_Relaxed = DATA_PATH + '/Mutated_Relaxed/' + WT_NAME + '_final_Relaxed.pdb',
    output:
        Shell_file = RUN_FILE + '/Manual.sh'
    params:
        Distance_py =  UTILS_PATH + '/MC/distance_DMS.py',
        WT_path = DATA_PATH + '/Cleaned_WT/' + WT_NAME + '_' + TARGET_CHAIN + '.pdb',
        Distance = DISTANCE,
        Chain = TARGET_CHAIN,
        Start_pos = PDB_START,
        End_pos = PDB_END,
        Out_path = DATA_PATH + '/Com_PM_DMS',
        Scripts_path = UTILS_PATH + '/MC/ComboPM_without.xml',
        Name = WORK_NAME,
        Node = NODE,
        Ntasks = NTASKS,
        Num = NUM,
        Ref_path = RUN_FILE + '/ref.txt',
        Python_path = PYTHON_PATH,
        In_site = IN_SITE
    shell:
        """
        {params.Python_path} {params.Distance_py}\
         --wt_path {params.WT_path}\
         --input_path {input.Final_Relaxed}\
         --distance {params.Distance}\
         --chain {params.Chain}\
         --start_pos {params.Start_pos}\
         --end_pos {params.End_pos}\
         --shell_path {output.Shell_file}\
         --out_path {params.Out_path}\
         --xml_path {params.Scripts_path}\
         --name {params.Name}\
         --node {params.Node}\
         --ntasks {params.Ntasks}\
         --ref_path {params.Ref_path}\
         --num {params.Num}\
         --in_site {params.In_site}
        """

rule Com_PM:
    input:
        RUN_FILE + '/Manual.sh'
    output:
        DATA_PATH + '/Com_PM_DMS/socre.sc'
    params:
        DATA_PATH + '/Com_PM_DMS'
    threads:
        THREADS
    shell:
        """
        mkdir -p {params} && sh {input}   
        """
