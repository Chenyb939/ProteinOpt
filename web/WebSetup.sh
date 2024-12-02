#!/bin/bash
set -e
setup_environment() {
    conda create -n Proteinopt_web python=3.8 --yes

    #  Check the Proteinopt_web conda environment
    if [ $? -ne 0 ]; then
        echo "Failed to create conda environment."
        return 1
    fi

    eval "$(conda shell.bash hook)"
    conda activate Proteinopt_web

    # Check if the environment has been activated successfully
    if [ $? -ne 0 ]; then
        echo "Failed to activate conda environment."
        return 1
    fi

    pip install flask
    pip install pymysql
    pip install flask-sqlalchemy
    pip install flask-migrate

    if [ $? -ne 0 ]; then
        echo "Failed to install packages."
        return 1
    fi

    echo "All packages installed successfully."
}

create_database() {
    read -p "Enter MySQL username: " mysql_user
    read -s -p "Enter MySQL password: " mysql_password
    echo

    # database name
    database_name="ProteinOpt"

    # Check if the MySQL service is running
    if ! mysqladmin ping -h"localhost" -u"$mysql_user" -p"$mysql_password" --silent; then
        echo "MySQL service is not running or credentials are incorrect."
        return 1
    fi

    # Create database
    mysql -h"localhost" -u"$mysql_user" -p"$mysql_password" -e "DROP DATABASE IF EXISTS \`${database_name}\`;"
    mysql -h"localhost" -u"$mysql_user" -p"$mysql_password" -e "CREATE DATABASE IF NOT EXISTS \`${database_name}\`;"

    # Check database
    if [ $? -eq 0 ]; then
        echo "Database '$database_name' created successfully."
    else
        echo "Failed to create database '$database_name'."
        return 1
    fi
}

setup_flask_app() {
    eval "$(conda shell.bash hook)"
    conda activate Proteinopt_web

    if [ -d "migrations" ]; then
    echo "Found the migrations folder, deleting..."
    # Delete the migrations folder and its contents
    rm -rf migrations
    fi

    # init database
    echo "begin to initialize the database."
    flask db init
    if [ $? -ne 0 ]; then
        echo "Failed to initialize the database."
        return 1
    fi

    # generate migration script
    echo "begin to generate migration script."
    flask db migrate
    if [ $? -ne 0 ]; then
        echo "Failed to generate migration script."
        return 1
    fi

    # upgrade the database
    echo "begin to upgrade the database."
    flask db upgrade
    if [ $? -ne 0 ]; then
        echo "Failed to upgrade the database."
        return 1
    fi

    echo "Database setup completed successfully."
}

# run Flask
start_app() {
    eval "$(conda shell.bash hook)"
    conda activate Proteinopt_web

    nohup python ./app.py > app.log 2>app.log &
    if [ $? -ne 0 ]; then
        echo "Failed to start the Flask app."
        return 1
    fi

    echo "Flask app started successfully."
}

# run process
start_process() {
    eval "$(conda shell.bash hook)"
    conda activate Proteinopt_web
    
    nohup python ./process.py > process.log 2>process.log &
    if [ $? -ne 0 ]; then
        echo "Failed to start the process script."
        return 1
    fi

    echo "Process script started successfully."
}

setup_environment
create_database
setup_flask_app
# start_app
# start_process
