from flask import abort, Blueprint, make_response, request, Response
from app.models.goal import Goal
from app.models.task import Task
from ..db import db
from .route_utilities import create_model, get_models_with_filters, validate_model

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal, request.args)

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    result = {}
    result["goal"] = goal.to_dict() # RE-EVALUATE THIS LATER
    return result

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.post("/<goal_id>/tasks")
def connect_task_to_goal(goal_id):
    
    goal = validate_model(Goal, goal_id)

    # try:
    #     goal_id == goal.id
    # except:
    #     response = {"message": f"Invalid request: ID given in path not equivalent to ID in request body."}
    #     abort(make_response(response, 400)) # CHECK THIS LATER WHAT RESPONSE CODE SHOULD I DO

    request_body = request.get_json() # this should be the dict w/ key: task_ids value: list of the ids
    tasks = []

    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        tasks.append(task)
    # If any of the task IDs are invalid, will abort before this point.
    # Assume we do not want to associate any of the tasks with the goal if *any*
    # of the IDs are invalid.
    
    for task in goal.tasks:
        # Unassociate previously associated tasks
        task.goal_id = None

    for task in tasks:
        task.goal_id = goal_id # only need to update FK in task item to create relationship

    db.session.commit()

    response_body = {
        "id": goal.id,
        "task_ids": request_body["task_ids"] # To reach this point, all the given IDs have been verified + relationship created.
    }
    return response_body, 200 # fix this later

@bp.get("/<goal_id>/tasks")
def get_tasks(goal_id): # getting tasks of one goal 
    goal = validate_model(Goal, goal_id)
    response_body = goal.to_dict()
    
    if not goal.tasks:
        response_body["tasks"] = [] # Do this to avoid issues with previous tests
    
    return response_body, 200