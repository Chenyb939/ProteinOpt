## Before You Begin

### Prerequisites

- **ProteinOpt Installation**: Before using the ProteinOpt WEB version, ensure that ProteinOpt is correctly installed by following the provided [installation guide](../README.md).
- **MySQL Installation** Ensure that the MySQL database is correctly installed (we have tested with version 8.0.36). For installation instructions, please refer to the [MySQL official documentation](https://dev.mysql.com/doc/).

### Quick Install
#### Step 1: Configure the Environment
Modify the configuration file (config.ini) for ProteinOpt. The configuration file should be set up according to the documentation.
``` ini
;Example config.ini contents
[WEB]
ip = 127.0.0.1 # Localhost
port = 5000

[DATABASE]
user = your_mysql_database_username
password = your_mysql_database_password

[PATH]
soft_dir = /path/to/your/project/bin
work_dir = /path/to/your/output/path
Rosetta_dir = /path/to/your/Rosetta
python_dir = /path/to/your/python
```
##### WEB Section
- **ip**: The IP address of the web server.
- **port**: The port number on which the web server will listen.
##### DATABASE Section
- **user**: The username for the MySQL database.
- **password**: The password for the MySQL database
##### PATH Section
- **soft_dir**: The directory path to the ProteinOpt software binaries.
- **work_dir**: The directory path where the software will perform its operations and output results.
- **Rosetta_dir**: The directory path to the Rosetta software.
- **python_dir**: The directory path to the Python environment required by ProteinOpt.

#### Step 2: Execute the installation and startup scripts
The `WebSetup.sh` script automates the setup of the ProteinOpt environment and the MySQL database configuration.
To execute the script, run the following command in your terminal:
```bash
./WebSetup.sh
```

#### Step 3: Launch the ProteinOpt Web Interface
To start the ProteinOpt web interface, run the `launchWeb.sh` script. This script will initiate the web server and make the interface accessible.
```bash
./launchWeb.sh
```
#### Notes
Ensure that the script has executable permissions before running it. You can grant these permissions with the `chmod +x` command.

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
