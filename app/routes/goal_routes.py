from flask import Blueprint, request, abort, make_response
from app.models.goal import Goal
from app.db import db
from app.routes.route_utilities import apply_filters, validate_model, set_new_attributes

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")


@bp.post("/", strict_slashes=False)
def create_goal():
    req_body = request.get_json()
    if "title" not in req_body:
        message = {"details": "Invalid data"}
        abort(make_response(message, 400))

    new_goal = Goal(req_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201


@bp.get("/", strict_slashes=False)
def get_all_goals():
    sort = request.args.get("sort")
    query = db.select(Goal).order_by(Goal.title.desc() if sort=="desc" else Goal.title)

    apply_filters(Goal, request.args.items(), query)

    goals = db.session.scalars(query)
    return [goal.to_dict() for goal in goals], 200


@bp.get("/<goal_id>", strict_slashes=False)
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return { "goal": goal.to_dict() }, 200


@bp.put("/<goal_id>", strict_slashes=False)
def update_goal(goal_id):
    req_body = request.get_json()
    goal = validate_model(Goal, goal_id)
    set_new_attributes(goal, req_body)

    db.session.commit()

    return { "goal": goal.to_dict() }, 200


@bp.delete("/<goal_id>", strict_slashes=False)
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal.id} "{goal.title}" successfully deleted'}, 200
