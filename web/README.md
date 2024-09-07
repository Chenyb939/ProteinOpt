## Before You Begin

### Prerequisites

- **ProteinOpt Installation**: Before using the ProteinOpt WEB version, ensure that ProteinOpt is correctly installed by following the provided [installation guide](../README.md).
- **MySQL Installation** Ensure that the MySQL database is correctly installed (we have tested with version 8.0.36). For installation instructions, please refer to the [MySQL official documentation](https://dev.mysql.com/doc/).
  
### Installation
To utilize ProteinOpt effectively, follow these steps:

#### Step 1: Install Conda Virtual Environment
First, ensure that Conda is installed on your system. Then, create a new virtual environment:

```bash
conda create -n Proteinopt_web python=3.8
conda activate Proteinopt_web
pip install flask
pip install pymysql
pip install flask-sqlalchemy
pip install flask-migrate
```
or
```bash
conda env create -f environment.yml
conda activate Proteinopt_web
```

#### Step 2: Create Mysql Database
Please make sure the mysql database is installed.Enter mysql to create a database named ProteinOpt
```
mysql -u root -p
```
Enter your password
```
create database ProteinOpt;
quit;
```

#### Step 3: Configure the Environment
Modify the configuration file (config.ini) for ProteinOpt. The configuration file should be set up according to the documentation.
``` ini
;Example config.ini contents
[database]
host = localhost
user = your_mysql_database_username
password = your_mysql_database_password
database = proteinopt_db

[paths]
soft_dir = /path/to/your/project/bin
work_dir = /path/to/your/output/path
Rosetta_dir = /path/to/your/Rosetta
python_dir = /path/to/your/python
```
** The database configuration remains unchanged.


#### Step 4: Start the Service
With the environment activated and the configuration set, you can now start the ProteinOpt service. Use the following command:

* Initialize the database and create a task table
``` bash
flask db init
flask db migrate
flask db upgrade
```
* Deploy web pages
```
screen -S web
conda activate Proteinopt_web
python app.py
```
* Deploy background services
```
screen -S opt
conda activate Proteinopt_web
python process.py
```

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
