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

start_app
start_process
