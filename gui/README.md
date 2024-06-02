## Before You Begin

### Prerequisites

- **ProteinOpt Installation**: Before using the ProteinOpt GUI version, ensure that ProteinOpt is correctly installed by following the provided [installation guide](../README.md).

### Useage
Users have the option to run the application using either of the following methods:

### On Windows:
Double-click the `.exe` file to start the application. Ensure that your system meets the necessary requirements to execute the program.

### On Linux:
Double-click the `.AppImage` file to launch the application. This format provides a portable, self-contained application image that is distributable and easy to use.

Please make sure that you have the appropriate permissions set for the `.exe` or `.AppImage` file to allow execution.

### Output files
   The downloaded ProteinOpt result package has the following folder structure:

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
   │       ├── Com_PM_VIP          The RosettaVIP protocol results
   │       ├── Com_PM_PM           The PMS protocol results
   │       ├── Com_PM_DMS          The Manual protocol results
   │       ├── Com_PM_41           The supercharge protocol results
   │       ├── Com_PM_42           The supercharge protocol (ues reference) results
   │       └── Cleaned_WT          The cleaned input file
   │
   └── data                        The input PDB file
   ```
