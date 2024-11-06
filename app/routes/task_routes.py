from flask import Blueprint, request, make_response, abort
from datetime import datetime
from app.models.task import Task
from app.db import db


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

    for attribute, value in request.args.items():
        if hasattr(Task, attribute):
            query = query.where(getattr(Task, attribute).ilike(f"%{value}%"))

    tasks = db.session.scalars(query)
    return [task.to_dict() for task in tasks], 200

@bp.get("/<task_id>", strict_slashes=False)
def get_one_task(task_id):
    task = validate_task(task_id)

    return { "task": task.to_dict() }, 200

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        message = { "message": f"Task ID {task_id} is invalid"}
        abort(make_response(message, 400))

    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if not task:
        message = {"message": f"Task with ID {task_id} was not found"}
        abort(make_response(message, 404))

    return task

@bp.put("/<task_id>", strict_slashes=False)
def update_task(task_id):
    req_body = request.get_json()
    req_body["completed_at"] = req_body.get("completed_at", None)
    task = validate_task(task_id)

    task.title = req_body["title"]
    task.description = req_body["description"]
    task.completed_at = req_body["completed_at"]

    db.session.commit()

    print({ "task": task.to_dict() })
    return { "task": task.to_dict() }, 200

@bp.delete("/<task_id>", strict_slashes=False)
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task.id} "{task.title}" successfully deleted'}, 200

@bp.patch("/<task_id>/mark_complete")
def mark_task_completed(task_id):
    task = validate_task(task_id)
    task.completed_at = datetime.now()
    db.session.commit()

    return { "task": task.to_dict() }, 200

@bp.patch("/<task_id>/mark_incomplete")
def mark_task_incompleted(task_id):
    task = validate_task(task_id)
    task.completed_at = None
    db.session.commit()

    return { "task": task.to_dict() }, 200