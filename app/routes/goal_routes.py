from flask import Blueprint, request, abort, make_response
from app.models.goal import Goal
from app.models.task import Task
from app.db import db
from app.routes.route_utilities import *

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")


@bp.post("/", strict_slashes=False)
def create_goal():
    return create_class_instance(Goal, request, ["title"])

@bp.get("/", strict_slashes=False)
def get_all_goals():
    return get_all_instances(Goal, request.args)

@bp.get("/<goal_id>", strict_slashes=False)
def get_one_goal(goal_id):
    return get_one_instance(Goal, goal_id)

@bp.put("/<goal_id>", strict_slashes=False)
def update_goal(goal_id):
    return update_instance(Goal, goal_id, request)

@bp.delete("/<goal_id>", strict_slashes=False)
def delete_goal(goal_id):
    return delete_instance(Goal, goal_id)

@bp.post("/<goal_id>/tasks")
def assign_task_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    task_ids = request.get_json().get("task_ids", [])
    list_of_tasks = []

    for task_id in task_ids:
        task = validate_model(Task, task_id)
        if task:
            list_of_tasks.append(task)

    goal.tasks.extend(list_of_tasks)
    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": [task.id for task in goal.tasks]
    }

@bp.get("/<goal_id>/tasks")
def get_task_of_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": [task.to_dict() for task in goal.tasks]
    }
