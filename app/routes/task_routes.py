from flask import Blueprint, request, make_response, abort
from datetime import datetime
from os import environ
import requests

from app.models.task import Task
from app.db import db
from app.routes.route_utilities import *

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@bp.post("/", strict_slashes=False)
def create_task():
    return create_class_instance(Task, request, ["title", "description"])

@bp.get("/", strict_slashes=False)
def get_all_tasks():
    return get_all_instances(Task, request.args)

@bp.get("/<task_id>", strict_slashes=False)
def get_one_task(task_id):
    return get_one_instance(Task, task_id)

@bp.put("/<task_id>", strict_slashes=False)
def update_task(task_id):
    return update_instance(Task, task_id, request)

@bp.delete("/<task_id>", strict_slashes=False)
def delete_task(task_id):
    return delete_instance(Task, task_id)

@bp.patch("/<task_id>/mark_complete")
def mark_task_completed(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()

    try:
        send_task_complete_message(task.title)

    except Exception as e:
        raise Exception("An error occurred during notification sending! Please connect to the Task List developer!") from e
    
    return { "task": task.to_dict() }, 200

@bp.patch("/<task_id>/mark_incomplete")
def mark_task_incompleted(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()

    return { "task": task.to_dict() }, 200

def send_task_complete_message(task_title):
    print(environ.get('SLACK_API_KEY'))
    request_data = {
    "channel": "#api-test-channel", # Slack channel for tests
    # "channel": "U07GC9C8Y4X", # My Slack account ID
    "username": "Task List app",
    "text": f"Someone just completed the task \"{task_title}\""
    }
    message_status = requests.post(
        url="https://slack.com/api/chat.postMessage", 
        json=request_data,
        headers={
            "Authorization": environ.get('SLACK_API_KEY'),
            "Content-Type": "application/json"
            },
        timeout=5
    )
    print(message_status)
    print('____________________________________________')
    # print(message_status.json()['message'])
    print(message_status.ok)
    print('____________________________________________')
    print(message_status.error)

    return message_status.json()["ok"]
