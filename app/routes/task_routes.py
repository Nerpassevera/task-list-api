from flask import Blueprint, request, make_response, abort
from datetime import datetime
from os import environ
import requests

from app.models.task import Task
from app.db import db
from app.routes.route_utilities import apply_filters, validate_model, set_new_attributes

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("/", strict_slashes=False)
def create_task():
    req_body = request.get_json()
    if "title" not in req_body or "description" not in req_body:
        message = {"details": "Invalid data"}
        abort(make_response(message, 400))
    new_task = Task.from_dict(req_body)

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@bp.get("/", strict_slashes=False)
def get_all_tasks():

    sort = request.args.get("sort")
    query = db.select(Task).order_by(Task.title.desc() if sort=="desc" else Task.title)

    apply_filters(Task, request.args.items(), query)

    tasks = db.session.scalars(query)
    return [task.to_dict() for task in tasks], 200

@bp.get("/<task_id>", strict_slashes=False)
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return { "task": task.to_dict() if task else task}, 200


@bp.put("/<task_id>", strict_slashes=False)
def update_task(task_id):
    req_body = request.get_json()
    req_body["completed_at"] = req_body.get("completed_at", None)
    task = validate_model(Task, task_id)

    set_new_attributes(task, req_body)
    print(*task.to_dict(), sep='\n')

    db.session.commit()
    return { "task": task.to_dict() }, 200

@bp.delete("/<task_id>", strict_slashes=False)
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task.id} "{task.title}" successfully deleted'}, 200

@bp.patch("/<task_id>/mark_complete")
def mark_task_completed(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()

    message_is_sent = send_task_complete_message(task.title)

    if not message_is_sent:
        raise Exception(
            "An error occured during notification sending!\
                Please connect to the Task List developer!")
    return { "task": task.to_dict() }, 200

@bp.patch("/<task_id>/mark_incomplete")
def mark_task_incompleted(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()

    return { "task": task.to_dict() }, 200

def send_task_complete_message(task_title):
    request_data = {
    # "channel": "#api-test-channel", # Slack channel for tests
    "channel": "U07GC9C8Y4X", # My Slack account ID
    "username": "Task List app",
    "text": f"Someone just completed the task \"{task_title}\""
    }
    message_status = requests.post(
        url="https://slack.com/api/chat.postMessage", 
        json=request_data,
        headers={"Authorization": environ.get('SLACK_API_KEY')},
        timeout=1
    )

    return message_status.json()["ok"]
