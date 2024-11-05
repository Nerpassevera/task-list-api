from flask import Blueprint, request
from app.models.task import Task
from app.db import db


bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("/", strict_slashes=False)
def create_task():
    req_body = request.get_json()
    req_body["completed_at"] = req_body.get("completed_at", None)
    new_task = Task.from_dict(req_body)

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@bp.get("/", strict_slashes=False)
def get_all_tasks():
    query = db.select(Task).order_by(Task.id)

    for attribute, value in request.args.items():
        if hasattr(Task, attribute):
            query = query.where(getattr(Task, attribute).ilike(f"%{value}%"))

    tasks = db.session.scalars(query)
    return [task.to_dict() for task in tasks], 200

@bp.get("/<task_id>", strict_slashes=False)
def get_one_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return {}
    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    return { "task": task.to_dict() }, 200
