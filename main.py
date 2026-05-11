#import all routing templates and request
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy  #for database opration 
from flask_login import (LoginManager,UserMixin,login_user,logout_user,login_required,current_user) 
from werkzeug.security import generate_password_hash, check_password_hash #Password hashing
from config import Config #database configuration file 
import pandas as pd #python freamwork libabry for analysis
import numpy as np
from flask_socketio import SocketIO # for live websocket


app = Flask(__name__)  #create a flask app  
socketio = SocketIO(app) #wesockt
app.config.from_object(Config) #load config from config.py

db = SQLAlchemy(app) #initzliation databse 

login_manager = LoginManager() #login manager 


login_manager.init_app(app)
login_manager.login_view = "login"  #redirect to login page 


class User(db.Model, UserMixin): 
    __tablename__ = "users"  #databse tbale name 

    id = db.Column(db.Integer, primary_key=True)  #--- primary key 
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  #email uniqe
    password = db.Column(db.String(255), nullable=False) #hasepassword 


class Task(db.Model):
    __tablename__ = "tasks" #database name task 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column
    priority = db.Column(db.String(50))
    status = db.Column(db.String(50), default="Pending")
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    #using foreign key with user id 


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#all endpoint start here 

@app.route("/") # login api 
def home(): 
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html") # render the register page 

    data = request.form  #get form data 

    if User.query.filter_by(email=data["email"]).first():  #check email exits or not 
        flash("Email alreaddy exits ")
        return redirect(url_for("login"))

    user = User(    #creating new users 
        username=data["username"],
        email=data["email"],
        password=generate_password_hash(data["password"])
    )

    #save in all data in databses 

    db.session.add(user)
    db.session.commit()

    flash("Registration successful.")
    
    return redirect(url_for("login"))



#login end point 

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")  #rensder login page 

    data = request.form
    user = User.query.filter_by(email=data["email"]).first()

#check password 
    if user and check_password_hash(user.password,data["password"]):
        login_user(user)
        return redirect(url_for("dashboard"))
    flash("Invalid email or password.")

    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("index.html", user=current_user)


@app.route("/api/tasks", methods=["POST"])
@login_required
def add_task():

    data = request.get_json()

    task = Task(
        title=data["title"],
        description=data["description"],
        priority=data["priority"],
        status=data.get("status", "Pending"),
        user_id=current_user.id
    )

    db.session.add(task)
    db.session.commit()

    socketio.emit("all_task_notifi", {
        "message": "Task added successfully"
    })

    return {
        "message": "Task added successfully",
        "task": all_task_include(task)
    }, 201
def all_task_include(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "status": task.status,
        "created_date": task.created_date.strftime("%Y-%m-%d %H:%M:%S")
    }



@app.route("/api/tasks", methods=["GET"])
@login_required
def get_tasks():

    tasks = Task.query.filter_by(user_id=current_user.id).all()

    return {"tasks": [all_task_include(task) for task in tasks]}, 200


def all_task_include(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "status": task.status,
        "created_date": task.created_date.strftime("%Y-%m-%d %H:%M:%S")
    }
#update end point 
@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
@login_required
def update_task(task_id):

    task = get_user_task(task_id)
    if not task:
        return {"error": "Task not found"}, 404

    data = request.get_json() #get data in json formate

    for field in [
        "title",
        "description",
        "priority",
        "status"
    ]:
        setattr(task, field, data.get(field, getattr(task, field)))

    db.session.commit()

    socketio.emit("all_task_notifi", {
        "message": "Task updated successfully"
    })

    return {"message": "Task updated successfully"}, 200


def get_user_task(task_id):
    return Task.query.filter_by(id=task_id,user_id=current_user.id).first()


#task delete ennd point 
@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):

    task = get_user_task(task_id)

    if not task:  
        return {"error": "Task not found"}, 404

    db.session.delete(task)
    db.session.commit()

    socketio.emit("all_task_notifi", {
        "message": "Task deleted successfully"
    })

    return {"message": "Task deleted successfully"}, 200


#analtytics end point 
@app.route("/api/analytics", methods=["GET"])
@login_required
def task_analytics():
    tasks = Task.query.filter_by(user_id=current_user.id).all()

    df = pd.DataFrame([  #create a dataframe for task and check data datarame 
        {
            "status": task.status
        }
        for task in tasks
    ])

    if df.empty:
        return {
            "total_tasks": 0,
            "completed_tasks": 0,
            "pending_tasks": 0,
            "completion_percentage": 0
        }, 200

    total = len(df)

    completed = len(df[df["status"] == "Completed"])

    pending = len(df[df["status"] == "Pending"])

    percentage = np.round((completed / total) * 100,2)

    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "completion_percentage": float(percentage)
    }, 200

#logout endpoint
@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    socketio.run(
        app,
        debug=True
    )