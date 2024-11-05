from flask import Blueprint, request
from app.models.task import Task
from app.db import db


bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks/")

@bp.post("")
def create_task():
    req_body = request.get_json()
    title = req_body["title"]
    description = req_body["description"]
    completed_at = req_body.get("completed_at", None)

    new_task = Task(
            title=title,
            description=description,
            completed_at=completed_at,
    )

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201
