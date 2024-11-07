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
