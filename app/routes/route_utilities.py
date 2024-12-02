from flask import abort, make_response
from app.db import db

def apply_filters(cls, arguments, query):
    for attribute, value in arguments:
        if hasattr(cls, attribute):
            query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))

def validate_model(cls, cls_id):
    try:
        cls_id = int(cls_id)
    except ValueError:
        message = { "message": f"{cls.__name__} ID {cls_id} is invalid"}
        abort(make_response(message, 400))

    query = db.select(cls).where(cls.id == cls_id)
    result = db.session.scalar(query)

    if not result:
        message = {"message": f"{cls.__name__} with ID {cls_id} was not found"}
        abort(make_response(message, 404))

    return result

def set_new_attributes(instance, req_body):
    for attr, value in req_body.items():
        if hasattr(instance, attr):
            setattr(instance, attr, value)

def create_class_instance(cls, request, required_fields):
    req_body = request.get_json()
    try:
        new_instance = cls.from_dict(req_body)
    except KeyError as error:
        message = {"details": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(message, 400))

    db.session.add(new_instance)
    db.session.commit()

    return {cls.__name__.lower(): new_instance.to_dict()}, 201

def get_all_instances(cls, args):
    sort = args.get("sort")
    query = db.select(cls).order_by(cls.title.desc() if sort=="desc" else cls.title)

    apply_filters(cls, args.items(), query)

    instances = db.session.scalars(query)
    return [instance.to_dict() for instance in instances], 200

def get_one_instance(cls, instance_id):
    instance = validate_model(cls, instance_id)

    return { cls.__name__.lower(): instance.to_dict() if instance else instance}, 200

def update_instance(cls, instance_id, request):
    instance = validate_model(cls, instance_id)
    req_body = request.get_json()
    if cls.__name__ == "Task":
        req_body["completed_at"] = req_body.get("completed_at", None)

    set_new_attributes(instance, req_body)

    db.session.commit()
    return { cls.__name__.lower(): instance.to_dict() }, 200

def delete_instance(cls, instance_id):
    instance = validate_model(cls, instance_id)
    db.session.delete(instance)
    db.session.commit()

    return {"details": f'{cls.__name__} {instance.id} "{instance.title}" successfully deleted'}, 200