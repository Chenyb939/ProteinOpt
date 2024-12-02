## ProteinOpt Application Setup Instructions

### Before You Begin

- **ProteinOpt Installation**: Before using the ProteinOpt GUI version, ensure that ProteinOpt is correctly installed by following the provided [installation guide](../README.md).

### Useage

1. **Download and Extract the Application:**
   - Users should begin by downloading the `ProteinOpt.zip` file from the `gui` directory.
   - Once downloaded, extract the contents of the `ProteinOpt.zip` file to a desired location on their system.

2. **Launch the Application:**
   - After extraction, locate and execute the `ProteinOpt` binary file to initiate the application.

3. **Initial Configuration:**
   - For first-time, it is essential to configure the application by accessing the 'Setting' interface.
   - Click the 'Setting' button to enter the configuration menu.

4. **Environment Setup:**
   - In the Settings interface, users are required to set up the necessary environment paths for the application to run correctly.
   - The following paths must be configured: the bin directory of the ProtionOpt, the bin directory of the Rosetta suite, the Python environment directory of ProtionOpt, and output  directory of ProtionOpt results.
   - Ensure that each path is set according to the specific requirements of the application and the user's system setup.
   - Users can select one of the four provided optimization techniques based on their specific needs.

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
