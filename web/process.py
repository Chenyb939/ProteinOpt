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
from pathlib import Path

def command1(command,task_id,log_file_path,Task,session):
    try:
        process = Popen(command,stdout=PIPE, stderr=PIPE, shell=True)
        process.wait()
        stdout, stderr = process.communicate()
        print("STDOUT:", stdout.decode())
        print("STDERR:", stderr.decode())
        if process.returncode == 0:
            return True

    except subprocess.CalledProcessError as e:
        print(f"Command 1 fails to run: {e}")
        return False
    except Exception as e:
        print(f"Command 1 fails to run: {e}")
        return False

    finally:
        file=os.path.join(log_file_path,str(task_id)+'.log')
        with open(file, 'a+') as log_file:
            if stdout:
                log_file.write("stdout:\n")
                log_file.write(stdout.decode())
            if stderr:
                log_file.write(f"\nTask {task_id}: Command 1 fails to run,The status was updated to error.")
                log_file.write("stderr:\n")
                log_file.write(stderr.decode())
            if process.returncode == 0:
                update_stmt = (
                    update(Task).
                    where(Task.c.id == task_id.split("_")[1]).
                    values(status='running')
                )
                update_result = session.execute(update_stmt)
                print(f"Task {task_id} :Command 1 is successfully run,The status was updated to running.")
                log_file.write(f"Task {task_id} :Command 1 is successfully run,The status was updated to running.")
            else:
                print(f"\nTask {task_id}: Command 1 fails to run,The status was updated to error.")
                update_stmt = (
                    update(Task).
                    where(Task.c.id == task_id.split("_")[1]).
                    values(status='error')
                )
                update_result = session.execute(update_stmt)
            session.commit()

def command2(command,task_id,log_file_path,Task,session):
    try:
        process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        process.wait()
        stdout, stderr = process.communicate()
        print("STDOUT:", stdout.decode())
        print("STDERR:", stderr.decode())
        if process.returncode == 0:
            return True

    except subprocess.CalledProcessError as e:
        return False
    except Exception as e:
        return False

    finally:
        file=os.path.join(log_file_path,str(task_id)+'.log')
        with open(file, 'a+') as log_file:
            if stdout:
                log_file.write("stdout:\n")
                log_file.write(stdout.decode())
            if stderr:
                log_file.write(f"\nTask {task_id}: Command 2 fails to run,The status was updated to error.")
                log_file.write("stderr:\n")
                log_file.write(stderr.decode())
            if process.returncode == 0:
                update_stmt = (
                    update(Task).
                    where(Task.c.id == task_id.split("_")[1]).
                    values(status='running')
                )
                update_result = session.execute(update_stmt)
                print(f"Command 2 is successfully run")
                log_file.write(f"Task {task_id} :Command 2 is successfully run,The status was updated to running.")
            else:
                print(f"\nTask {task_id}: Command 2 fails to run,The status was updated to error.")
                update_stmt = (
                    update(Task).
                    where(Task.c.id == task_id.split("_")[1]).
                    values(status='error')
                )
                update_result = session.execute(update_stmt)
            session.commit()


def command3(command,task_id,log_file_path,Task,session):
    try:
        process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        process.wait()
        stdout, stderr = process.communicate()
        print("STDOUT:", stdout.decode())
        print("STDERR:", stderr.decode())
        if process.returncode == 0:
            return True

    except subprocess.CalledProcessError as e:
        return False
    except Exception as e:
        return False

    finally:
        file=os.path.join(log_file_path,str(task_id)+'.log')
        with open(file, 'a+') as log_file:
            if stdout:
                log_file.write("stdout:\n")
                log_file.write(stdout.decode())
            if stderr:
                log_file.write(f"\nTask {task_id}: Command 3 fails to run,The status was updated to error.")
                log_file.write("stderr:\n")
                log_file.write(stderr.decode())
            if process.returncode == 0:
                update_stmt = (
                    update(Task).
                    where(Task.c.id == task_id.split("_")[1]).
                    values(status='complete')
                )
                update_result = session.execute(update_stmt)
                print(f"Task {task_id} :Command 3 is successfully run")
                log_file.write(f"Task {task_id} :Command 3 is successfully run,The status was updated to done.")
            else:
                print(f"\nTask {task_id}: Command 3 fails to run,The status was updated to error.")
                update_stmt = (
                    update(Task).
                    where(Task.c.id == task_id.split("_")[1]).
                    values(status='error')
                )
                update_result = session.execute(update_stmt)
            session.commit()


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

def find_and_update_task():
    engine = create_engine(DATABASE_URI, echo=False)
    metadata = MetaData()
    Task = Table('task', metadata, autoload_with=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    a_task = session.query(Task).filter(Task.c.status == 'waiting').first()
    if not a_task:
        print("no task is waiting")
        return 0;
    #print("Task information",a_task)
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
    log_file_path = os.path.join(work_dir, "log")
    if not os.path.exists(log_file_path):
        os.makedirs(log_file_path)

    if task_type=='pm':
        pm_seeds=task_content['seeds']
        command = f'{python_path} {script_path} --job_name {task_name} --input_file {task_file} ' \
                  f'--target_chain {task_chain} --ntasks {task_threads} --num {task_result} ' \
                  f'--top_pm_num {pm_seeds} --Rosetta_dir {Rosetta_path} --output_dir {work_dir} --proteinopt_bin {soft_dir+"/bin"} --python_path {python_path}'
    if task_type=="vip":
        command = f'{python_path}  {script_path} --job_name {task_name} --input_file {task_file} ' \
                  f'--target_chain {task_chain} --ntasks {task_threads} --num {task_result} ' \
                  f'--Rosetta_dir {Rosetta_path} --output_dir {work_dir} --proteinopt_bin {soft_dir+"/bin"} --python_path {python_path}'
    if task_type=="charge":
        vip_objective=task_content['objective']
        vip_charge = task_content['charge']
        command = f'{python_path}  {script_path} --job_name {task_name} --input_file {task_file} ' \
                  f'--target_chain {task_chain} --ntasks {task_threads} --num {task_result} ' \
                  f'--super_method {vip_objective} --super_target {vip_charge} --Rosetta_dir {Rosetta_path} ' \
                  f'--output_dir {work_dir} --proteinopt_bin {soft_dir+"/bin"} --python_path {python_path}'
    if task_type=="manally":
        manally_sites = task_content['sites'].replace(" ", "")
        manally_sites = re.sub(r'([a-zA-Z])\B(\d+)', r'\2', manally_sites).upper()
        # print(manally_sites)
        command = f'{python_path}  {script_path} --job_name {task_name} --input_file {task_file} ' \
                  f'--target_chain {task_chain} --ntasks {task_threads} --num {task_result} ' \
                  f'--in_site {manally_sites} --Rosetta_dir {Rosetta_path} --output_dir {work_dir} --proteinopt_bin {soft_dir+"/bin"} --python_path {python_path}'
    print("Submitted task content",task_content)
    print("Program command:",command)
    flag = command1(command, task_name, log_file_path,Task,session)

    if flag:
        os.chdir(os.path.join(work_dir, task_name, 'snakemake'))
        print("Current working directory:",os.getcwd())
        py_path = Path(python_path)
        env_name = py_path.parents[1].name
        print("Environment name:", env_name)
        command = f"conda run -n {env_name} bash {work_dir}/{task_name}/snakemake/preprocess.sh"
        flag = command2(command, task_name, log_file_path,Task,session)

    if flag:
        py_path = Path(python_path)
        conda_path = os.path.join(py_path.parents[3], "bin", "activate")
        env_name = py_path.parents[1].name
        print("Environment name:", env_name)
        if task_type=='pm':
            command = f"conda run -n {env_name} bash {work_dir}/{task_name}/snakemake/PMS.sh"
        if task_type=="vip":
            command = f"conda run -n {env_name} bash {work_dir}/{task_name}/snakemake/RosettaVIP.sh"
        if task_type=="charge":
            command = f"conda run -n {env_name} bash {work_dir}/{task_name}/snakemake/Supercharge_ref.sh"
        if task_type=="manally":
            command = f"conda run -n {env_name} bash {work_dir}/{task_name}/snakemake/Manual.sh"
        os.chdir(os.path.join(work_dir, task_name, 'snakemake'))
        flag = command3(command, task_name, log_file_path,Task,session)

def main():
    while True:
        find_and_update_task()
        time.sleep(20)

if __name__ == '__main__':
    main()
