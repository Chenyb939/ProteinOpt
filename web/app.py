import json
import os
import time
import re
import zipfile

import sqlalchemy
from datetime import datetime
from sqlalchemy.dialects.mysql import JSON
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, jsonify, Response, flash, send_file
from flask_migrate import Migrate
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
work_dir = config.get('PATH', 'work_dir')
# host = config.get('DATABASE', 'host')
host = "localhost"
user = config.get('DATABASE', 'user')
password = config.get('DATABASE', 'password')

web_ip = config.get('WEB', 'ip')
web_port = config.get('WEB', 'port')

app=Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}:3306/ProteinOpt?charset=utf8mb4'

db=SQLAlchemy(app)
migrate=Migrate(app,db)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    submit_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    work_dir = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    submit_content = db.Column(JSON, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'submit_time': self.submit_time.isoformat(),
            'work_dir': self.work_dir,
            'status': self.status,
            'submit_content': self.submit_content
        }


def is_valid_filename(filename):
    if not filename:
        return False
    if filename.startswith('.') and len(filename) == 1:
        return False
    if re.search(r'[/*?\(\)\[\]\{\}><|:"\'\\]', filename):
        return False
    if ' ' in filename:
        return False
    if len(filename) > 255:
        return False
    return True

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/example")
def example():
    return render_template("example.html")

@app.route("/help")
def help():
    return render_template("help.html")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/charge",methods=['get','post'])
def submit_charge():
    return render_template("submit_charge.html")

@app.route("/manally",methods=['get','post'])
def submit_manally():
    return render_template("submit_manally.html")

@app.route("/pm",methods=['get','post'])
def submit_pm():
    return render_template("submit_pm.html")

@app.route("/vip",methods=['get','post'])
def submit_vip():
    return render_template("submit_vip.html")

@app.route("/workspace",methods=['post'])
def workspace():
    data_dict = [{},{},{}]
    form_data = request.form.to_dict()
    content = json.dumps(form_data, ensure_ascii=False)
    print("Submitted task content",content)
    job_name=request.form.get('job_name')
    userID = request.form.get('localStorageData')

    user_count = Task.query.filter(Task.username==userID,Task.status != 'delete').count()
    if user_count < 3:
        submit_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        task_path = os.path.join(work_dir,'task',job_name, submit_time)
        if not os.path.exists(task_path):
            os.makedirs(task_path)
        file = request.files['pdb_file']
        if is_valid_filename(file.filename):
            file_path = os.path.join(work_dir,task_path,'uploads')
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file.save(os.path.join(file_path, file.filename))
        else:
            return "<h1>Sorry, The file name is not standardized</h1>"

        task=Task(username=userID,name=job_name,submit_time=submit_time,work_dir=task_path,status='waiting',submit_content=content)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('toMyWorkspace'))
    else:
        return "<h1>Sorry, each user can only submit three tasks</h1>"

@app.route('/remove/<id>/')
def remove(id):
    print("Task id:",id)
    user_data = Task.query.get(id)
    user_data.status="delete"
    db.session.commit()
    return redirect(url_for("toMyWorkspace"))

@app.route('/download')
def download():
    id = request.args.get('id', default='', type=str)
    jobname = request.args.get('jobname', default='', type=str)
    file_path=os.path.join(work_dir,jobname+'_'+id,'output')
    success_file=os.path.join(file_path,"success.log")
    zip_path = os.path.join(work_dir,jobname+'_'+id,'output.zip')
    print("The result directory of the task",file_path)
    if not os.path.exists(success_file):
        return "<h1>Sorry, The program has not finished running, the file is not available for download</h1>"
    else:
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(file_path, arcname=os.path.basename(file_path))
        return send_file(zip_path, as_attachment=True)

@app.route("/toMyWorkspace")
def toMyWorkspace():
    return render_template("to_workspace.html")

@app.route("/MyWorkspace",methods=['get','post'])
def my_workspace():
    data = request.json
    userID = data.get('uuid')
    data_dict = [{}, {}, {}]
    print("UserID:",userID)
    user_datas = Task.query.filter(Task.username==userID,Task.status != 'delete').all()
    num = len(user_datas)
    print("Number of submitted tasks",num)
    for i in range(0, len(user_datas)):
        data_dict[i] = user_datas[i].to_dict()
        data_dict[i]['submit_time'] = data_dict[i]['submit_time'].replace('T', ' ')
    html_content = render_template("workspace.html",data_dict=data_dict)
    return jsonify({'htmlContent': html_content})

if __name__=='__main__':
    # app.run()
    app.run(host=str(web_ip), port=int(web_port))