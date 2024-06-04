import subprocess
import re
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import select, update
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from subprocess import Popen, PIPE
import os
import json
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
work_dir = config.get('PATH', 'work_dir')
soft_dir = config.get('PATH', 'soft_dir')
python_path=config.get('PATH', 'python_dir')
Rosetta_path=config.get('PATH', 'Rosetta_dir')
host = config.get('DATABASE', 'host')
user = config.get('DATABASE', 'user')
password = config.get('DATABASE', 'password')

DATABASE_URI = f'mysql+pymysql://{user}:{password}@{host}:3306/ProteinOpt?charset=utf8mb4'
engine = create_engine(DATABASE_URI,echo=False)
metadata = MetaData()
Task = Table('task', metadata, autoload_with=engine)
Session = sessionmaker(bind=engine)
session = Session()

def find_and_update_task():
    a_task = session.query(Task).filter(Task.c.status == 'waiting').first()
    if not a_task:
        print("no task is waiting")
        return 0;
    print("Task information",a_task)
    task_id = str(a_task.id)
    task_name = str(a_task.name)+'_'+task_id
    task_dir = os.path.join(str(a_task.work_dir), 'uploads')
    file_name = os.listdir(task_dir)[0]
    task_file=os.path.join(task_dir, file_name)
    task_content=json.loads(a_task.submit_content)
    task_chain=task_content['chain']
    task_type=task_content['task']
    task_result = task_content['results_number']
    task_threads = task_content['threads_number']
    script_path = os.path.join(soft_dir, 'stab_dp.py')

    if task_type=='pm':
        pm_seeds=task_content['seeds']
        command = f'{python_path} {script_path} --job_name {task_name} --input_file {task_file} ' \
                  f'--target_chain {task_chain} --ntasks {task_threads} --num {task_result} ' \
                  f'--top_pm_num {pm_seeds} --Rosetta_dir {Rosetta_path} --output_dir {work_dir} --proteinopt_bin {soft_dir+"/bin"}'
    if task_type=="vip":
        command = f'{python_path}  {script_path} --job_name {task_name} --input_file {task_file} ' \
                  f'--target_chain {task_chain} --ntasks {task_threads} --num {task_result} ' \
                  f'--Rosetta_dir {Rosetta_path} --output_dir {work_dir} --proteinopt_bin {soft_dir+"/bin"}'
    if task_type=="charge":
        vip_objective=task_content['objective']
        vip_charge = task_content['charge']
        command = f'{python_path}  {script_path} --job_name {task_name} --input_file {task_file} ' \
                  f'--target_chain {task_chain} --ntasks {task_threads} --num {task_result} ' \
                  f'--super_method {vip_objective} --super_target {vip_charge} --Rosetta_dir {Rosetta_path} ' \
                  f'--output_dir {work_dir} --proteinopt_bin {soft_dir+"/bin"}'
    if task_type=="manally":
        manally_sites = task_content['sites'].replace(" ", "")
        manally_sites = re.sub(r'([a-zA-Z])\B(\d+)', r'\2', manally_sites).upper()
        # print(manally_sites)
        command = f'{python_path}  {script_path} --job_name {task_name} --input_file {task_file} ' \
                  f'--target_chain {task_chain} --ntasks {task_threads} --num {task_result} ' \
                  f'--in_site {manally_sites} --Rosetta_dir {Rosetta_path} --output_dir {work_dir} --proteinopt_bin {soft_dir+"/bin"}'
    print("Submitted task content",task_content)
    print("Program command:",command)

    process = Popen(command,stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    print("STDOUT:", stdout.decode())
    if process.returncode == 0:
        update_stmt = (
            update(Task).
            where(Task.c.id == task_id).
            values(status='running')
        )
        update_result = session.execute(update_stmt)
        print(f"The task {a_task.id} is running successfully and the status is updated to running.")
    else:
        update_stmt = (
            update(Task).
            where(Task.c.id == task_id).
            values(status='error')
        )
        update_result = session.execute(update_stmt)
        print(f"The task {a_task.id}  run failure and the status is updated to error.")
        print(f"Error message: {stderr.decode().strip()}")

    session.commit()

    os.chdir(os.path.join(work_dir, task_name, 'snakemake'))
    print("Current working directory:",os.getcwd())
    command = f"conda run -n opt bash {work_dir}/{task_name}/snakemake/preprocess.sh"
    result1 = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("Command 1 is executed successfully:", result1.stdout)
    if result1.returncode == 0:
        command = f"bash {work_dir}/{task_name}/snakemake/preprocess.sh"
        try:
            result2 = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result2.returncode == 0:
                print("Command 2 is executed successfully", result2.stdout)
                update_stmt = (
                    update(Task).
                    where(Task.c.id == task_id).
                    values(status='completed')
                )
                update_result = session.execute(update_stmt)
        except subprocess.CalledProcessError as e:
            print("Command 2 fails to be executed, and an error message is displayed：", e.stderr)
            update_stmt = (
                update(Task).
                where(Task.c.id == task_id).
                values(status='error')
            )
            update_result = session.execute(update_stmt)
    else:
        update_stmt = (
            update(Task).
            where(Task.c.id == task_id).
            values(status='error')
        )
        update_result = session.execute(update_stmt)
        print(f"Command 1 fails to be executed, and an error message is displayed")
        print(f"{stderr.decode().strip()}")


def main():
    while True:
        find_and_update_task()
        time.sleep(10)

if __name__ == '__main__':
    main()