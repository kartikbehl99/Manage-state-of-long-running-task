from flask import request, Blueprint, send_file
from app.modules.mod_user.user import User
from threading import Thread
import logging

export_route = Blueprint("export_route", __name__)

user = None

@export_route.route("/export", methods=["POST"])
def export():
    body = request.get_json()
    user_id = body["userID"]

    global user
    user = User(user_id)

    def task():
        user.obj2.export()
    
    thread = Thread(target=task)
    thread.start()

    return {
        "Status": "Started"
    }

@export_route.route("/export/pause", methods=["POST"])
def pause():
    status = user.obj2.get_status()
    if not status:
        user.obj2.pause()
        return {
            "Status": "Paused"
        }
    
    else:
        return {
            "Message": "Cannot pause, task already completed"
        }


@export_route.route("/export/resume", methods=["POST"])
def resume():
    def task():
        user.obj2.resume()
    
    thread = Thread(target=task)

    thread.start()

    return {
        "Status": "Resumed"
    }

@export_route.route("/export/download", methods=["GET"])
def download():
    status = user.obj2.get_status()
    if status:
        try:
            return send_file("../user1.csv", mimetype="text/csv", attachment_filename="user1.csv", as_attachment=True)
        except OSError:
            logging.error("404")
            return {
                "Status": "Error"
            }

    else:
        return {
            "Status": "Please Wait"
        }


@export_route.route("/export/terminate", methods=["POST"])
def terminate():
    user.obj2.terminate()
    return {
        "Status": "terminated"
    }