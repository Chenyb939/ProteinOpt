# ProteinOpt: Protein Stability Optimization Tool

ProteinOpt is a protein stability optimization tool based on Rosetta, designed to assist researchers and bioinformaticians in improving protein structures and stability. This tool offers four distinct protein optimization methods, including:

1. **Point Mutation Scanning**: Point Mutation Scanning involves mutating amino acids that are either recorded in wet lab experiments or manually marked. It employs a multi-point mutation approach to discover the most stable protein conformation.

2. **Mutation Cluster**: In Mutation Cluster, the aim is to identify amino acids that, when subjected to single-point saturation mutagenesis, result in the most significant reduction in sequence energy. Subsequently, a multi-point mutation method is used to find the most stable protein conformation based on these identified amino acids.
   
3. **Supercharge**: Supercharge focuses on mutating polar amino acids within the input protein to find the lowest/highest electrostatic potential. It then utilizes a multi-point mutation approach based on the mutated amino acids to discover the most stable protein conformation.
   
4. **RosettaVIP**: RosettaVIP calculates protein cavities within the input protein and fills them with mutations. It employs a multi-point mutation approach based on these mutated amino acids to search for the most stable protein conformation.

## Installation

To get started with ProteinOpt, follow these steps:

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/ProteinOpt.git
   ```
2. Navigate to the project directory:
   ```bash
   cd ProteinOpt
   ```
3. Creat irtual environment and install the required dependencies:
   ```bash
   conda activate ProteinOpt python=3.10
   activate ProteinOpt
   pip install snakemake biopython pandas
   ```
4. install Rosetta and PyRosetta 
   
   You can visit the [Rosetta](https://www.rosettacommons.org/software/license-and-download) website and download the Rosetta and PyRosetta Software Suite.

   Then, use the following command to configure the Rosetta environment variables.
   ```bash
   export PATH=$PATH:/path/to/rosetta/source/bin
   export ROSETTA=$ROSETTA:/path/to/rosetta
   export PATH=$ROSETTA_BIN:/path/to/rosetta/source/bin
   ```
   
## How to Use

To utilize ProteinOpt effectively, follow these steps:
1. Start by running the `stab_dp.py` script. This script is responsible for processing input files and generating the necessary files required for running ProteinOpt:
   ```bash
   usage: python stab_dp.py [--job_name] [--input_file] [--target_chain] [--node] [--ntasks] [--num] [--top_pm_num] [--in_site] [--super_method] [--super_target]

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
   ```
2. After running, you can open the `./[job_name]/config.yaml` file to view and modify the required configurations.
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
   ```bash 
   # Run single-point saturation mutagenesis scanning with the following command:
   bash ./[job_name]/snakemake/run1.sh
   # Perform Point Mutation Scanning optimization using the following command:
   bash ./[job_name]/snakemake/run2.sh
   # Execute Point Mutation Scanning optimization with the following command:
   bash ./[job_name]/snakemake/run3.sh
   # Initiate Supercharge optimization using the following command:
   bash ./[job_name]/snakemake/run4.1.sh
   # Initiate Supercharge optimization using the following command:
   bash ./[job_name]/snakemake/run4.2.sh
   # Launch RosettaVIP optimization with the following command:
   bash ./[job_name]/snakemake/run5.sh
   ```
4. Check the optimization results.
   
   Check the optimization results in the `./[job_name]/output/data` folder.

   To generate a summary file of the analysis results, please run the following command in your terminal:
   ```bash
   python analy.py
   ```

## Contributions

Contributions of code, issue reports, or improvement suggestions are welcome.
