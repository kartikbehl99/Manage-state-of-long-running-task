from flask import request, Blueprint
from app.modules.mod_user.user import User
from threading import Thread

insert_route = Blueprint("insert_route", __name__)

user = None
roll_back_checkpoint = None

@insert_route.route("/insert", methods=["POST"])
def insert():
    body = request.get_json()
    user_id = body["userID"]

    global user
    user = User(user_id)

    global roll_back_checkpoint
    roll_back_checkpoint = user.obj1.get_checkpoint()

    def task():
        user.obj1.start()

    thread = Thread(target=task)
    thread.start()
    
    return {
        "Status": "Started"
    } 


@insert_route.route("/insert/pause", methods=["POST"])
def pause():
    user.obj1.pause()
    
    return {
        "Status": "Paused"
    }


@insert_route.route("/insert/resume", methods=["POST"])
def resume():
    def task():
        user.obj1.resume()

    thread = Thread(target=task)
    thread.start()

    return {
        "Status": "Resumed"
    }


@insert_route.route("/insert/progress", methods=["GET"])
def progress():
    progress = user.obj1.get_progress()
    return {
        "progress": progress
    }

@insert_route.route("/insert/terminate", methods=["POST"])
def terminate():
    user.obj1.terminate(roll_back_checkpoint)
    return {
        "Status": "Terminated"
    }