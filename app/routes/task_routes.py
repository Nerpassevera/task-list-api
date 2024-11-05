from flask import Blueprint, request
from app.models.task import Task
from app.db import db


bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks/")
