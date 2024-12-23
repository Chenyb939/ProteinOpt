[![DOI](https://zenodo.org/badge/697241047.svg)](https://zenodo.org/doi/10.5281/zenodo.12748028)
# ProteinOpt: Protein Stability Optimization Tool

ProteinOpt is a multi-objective optimization tool specifically designed for vaccine antigens and decoys, leveraging the Rosetta software suite and Snakemake. ProteinOpt is designed to assist researchers in conveniently and swiftly conducting protein stability optimization operations using local resources. ProteinOpt offers four distinct protein optimization methods, including:


1. **Point Mutation Scanning**: Point Mutation Scanning identifies the seed residues by recording the amino acid with the most reduced energy in the sequence during single-point saturation mutations. During the single-point saturation mutation, ProteinOpt refrains from recording any information regarding the energy reduction associated with cysteine (C) to ensure that there is no substantial alteration to the protein structure. Subsequently, a multi-point mutation method is used to find the most stable protein conformation based on these identified amino acids.
   
2. **RosettaVIP**: RosettaVIP calculates protein cavities within the input protein and fills them with mutations. It employs a multi-point mutation approach based on these mutated amino acids to search for the most stable protein conformation.

3. **Supercharge**: Supercharge focuses on mutating polar amino acids within the input protein to find the lowest/highest electrostatic potential. After running Supercharge protocol, there will be two types of result files. One is the **reference file** that records which amino acids can increase or decrease the electrostatic potential of the input protein, and the other is the **mutated protein file**. During multi-point mutation approach, you can choose which result to use for optimization based on your needs. When using the reference file, the system has a larger search space and higher randomness. When using the mutated protein file, the system has shorter running time and more conservative results.
   
4. **Manually Specified Seed Residues**: Manually Specified Seed Residuescan can be selected based on experimental records and literature references to determine the amino acids that need to be mutated. ProteinOpt can utilize these residues for multi-point mutation methods to discover the most stable protein conformation.



## Installation

To get started with ProteinOpt, follow these steps:

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/Chenyb939/ProteinOpt.git
   ```
2. Navigate to the project directory:
   ```bash
   cd ProteinOpt
   ```
3. Creat irtual environment and install the required dependencies:
   
   For the convenience of subsequent installation of related dependencies such as PyRosetta, we recommend using Python versions 3.6, 3.7, 3.8, and 3.9
   ```bash
   conda create -n ProteinOpt python=3.9
   conda activate ProteinOpt
   pip install snakemake biopython pandas xlwt
   pip install pulp==2.7.0
   ```
4. Install Rosetta and PyRosetta
   
   For installation on Linux machines, you can follow the tutorials on the Rosetta. 
   If you intend to install the Rosetta software suite on an HPC system, please contact your system administrator. 

   After installation, use the following command to configure the Rosetta environment variables.
   ```bash
   export PATH=$PATH:/path/to/rosetta/source/bin
   export ROSETTA=$ROSETTA:/path/to/rosetta
   export ROSETTA_BIN=$ROSETTA_BIN:/path/to/rosetta/source/bin
   ```
   
## How to Use
For command-line execution, please follow the instructions in this document.  
For GUI users, access the [GUI Manual](gui/README.md).   
Web interface users should refer to the [Web Manual](web/README.md).


ProteinOpt can be thought of as a two-step pipeline. In the initial step, users can utilize three classic Rosetta protocols to find seed residue(s), including point mutation scanning, RosettaVIP (Void Identification and Packing), and Supercharge. Besides, users can also manually specify seed residue(s) as input. In the second step, ProteinOpt applies the mutation cluster protocol to further refine the conformation of the protein. 

To utilize ProteinOpt effectively, follow these steps:
1. Initial step
   Start by running the `stab_dp.py` script. This script is responsible for processing input files and generating the necessary files required for running.
   
   ```bash
   usage: python stab_dp.py [--job_name] [--input_file] [--target_chain] [--node] [--ntasks] [--num] [--top_pm_num] [--in_site] [--super_method] [--super_target] [--Rosetta_dir] [--proteinopt_bin] [--python_path]

   optional arguments:
      --job_name              Task Name
      --input_file            Path to the PDB file for optimization
      --target_chain          Target chain to be optimized
      --node                  Number of nodes used in the task (if on HPC, else 1)
      --ntasks                Number of threads/cores used in the task
      --num                   Number of generated optimized protein structures (default:5000)
      --top_pm_num            Number of amino acids with decreased energy (if use Point Mutation Scanning protocol; default: 10)
      --in_site               Documented mutation sites (if use Mutation Cluster protocol; default: 498R)
      --super_method          Supercharge methods (if use Supercharge protocol; default: residue)
      --super_target          Supercharge target (if use Supercharge protocol; default: positive)
      --Rosetta_dir           Path to the ROSETTA software
      --proteinopt_bin        The bin directory of ProteinOpt
      --python_path           The ProteinOpt python environment path
   ```
2. Check optimization configurations
   After running, you can open the `./[job_name]/config.yaml` file to view and modify the required configurations.
   ```
   ROSETTA:                   Directory of the installed Rosetta suite
   ROSETTA_BIN:               Bin directory of the Rosetta suite
   WORK_NAME:                 Task Name
   WT_NAME:                   PDB file name
   WORK_DIR:                  Directory of the files generated during runtime
   INPUT_DIR:                 Input directory of the PDB files
   OUTPUT_DIR:                Output directory
   RUN_DIR:                   Snakemake script directory
   UTILS_PATH:                Directory of the script being used during runtime
   DATA_PATH:                 Directory of the PDB output files
   RUN_FILE:                  Directory of the generated during runtime
   PYTHON_PATH:               Absolute path of Python used
   ALL_CHAINS:                Chains contained in the input PDB file
   TARGET_CHAIN:              Target chain to be optimized
   ANOTHER_CHAIN:             Chains excluded from optimization
   DISTANCE:                  Optimization range in units of Ångströms (Å)
   PDB_START:                 Starting position of the chain to be optimized
   PDB_END:                   Ending position of the chain to be optimized
   THREADS:                   Number of threads/cores used in the task
   NODE:                      Number of nodes used in the task
   NTASKS:                    Number of threads/cores used by each node in the task
   NUM:                       Number of generated optimized protein structures
   PM_NUM:                    Number of iterations for single-point saturation mutagenesis
   PDB_TOTAL:                 Number of amino acids in the target optimization chain
   TARGET_METHOD:             Supercharge methods (residue, atom)
   TARGET_CHARGE:             Supercharge target (positive, negative)
   TOP_PM_NUM:                Number of the top amino acids picked with the most energy redcution
   IN_SITE:                   Documented mutation sites
   ```

3. Submit your optimization tasks using the provided bash script:

   ProteinOpt optimization is divided into two steps. The first step involves preprocessing, while the second step allows you to choose the corresponding optimization strategy to run. Before running, please ensure that the parameters have been set correctly.
   
   Preprocessing step:
   ```bash 
   bash ./[job_name]/snakemake/preprocess.sh
   ```
   Optimization step:

   ```bash 
   # Perform Point Mutation Scanning optimization using the following command:
   bash ./[job_name]/snakemake/PMS.sh
   # Initiate Supercharge optimization using the following command:
   bash ./[job_name]/snakemake/Supercharge.sh
   # Initiate Supercharge optimization (reference base) using the following command:
   bash ./[job_name]/snakemake/Supercharge_ref.sh
   # Launch RosettaVIP optimization with the following command:
   bash ./[job_name]/snakemake/RosettaVIP.sh
   # Execute Manually Specified Seed Residues optimization with the following command:
   bash ./[job_name]/snakemake/Manual.sh
   ```

   After optimizing the input protein, ProteinOpt automatically creates a folder named after the task within the output path. The file structure is as follows:

   ``` 
   [job_name]
   │
   ├── utils                       Script used during runtime
   │   ├── VIP             
   │   ├── Supercharge     
   │   ├── relax           
   │   ├── PM              
   │   └── mutate          
   │
   ├── sankemake                   Files used during optimization
   │
   ├── output
   │   ├── utils                   Script generated during runtime
   │   └── data                    The output files during the optimization
   │       ├── WT                  The input PDB file
   │       ├── Supercharge         The Supercharge script result 
   │       ├── Relaxed_WT          The relax result of input PDB file
   │       ├── PM                  The Single-point mutation scanning result
   │       ├── Mutated             The mutated file after find seed residues
   │       ├── Mutated_Relaxed     The relax result of mutated file
   │       ├── Com_VIP             The RosettaVIP protocol results
   │       ├── Com_PMS             The PMS protocol results
   │       ├── Com_Manual          The Manual protocol results
   │       ├── Com_Super           The supercharge protocol results
   │       ├── Com_SuperREF        The supercharge protocol (ues reference) results
   │       └── Cleaned_WT          The cleaned input file
   │
   └── data                        The input PDB file
   ```

4. Check the optimization results.
   
   After optimization, you can check the optimization results in the `./[job_name]/output/data` folder.

   To generate a summary file of the analysis results, please run the following command in your terminal:

   ```bash
   usage: python analyse.py [--relaxed_path] [--Opt_dir] [--Out_dir] [--mut_sites]

   optional arguments:
      --relaxed_path          The input file after relax
      --Opt_dir               ProteinOpt optimized path
      --Out_dir               Output path for analysis results
      --mut_sites             Manually specified mutation sites (if use manual protocol)
   ```


## Contributions

Contributions of code, issue reports, or improvement suggestions are welcome.
