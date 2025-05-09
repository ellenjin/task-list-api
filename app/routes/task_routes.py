from flask import abort, Blueprint, make_response, request, Response
from app.models.task import Task
from ..db import db
from .route_utilities import create_model, get_models_with_filters, validate_model
from datetime import datetime
from .slack_routes import send_slack_notification

bp = Blueprint("task_list_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

@bp.get("")
def get_all_tasks():
    return get_models_with_filters(Task, request.args)

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    result = {}
    result["task"] = task.to_dict() # RE-EVALUATE THIS LATER
    return result

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# Wave 3
@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()

    send_slack_notification(f"Someone just completed the task {task.title}")

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")