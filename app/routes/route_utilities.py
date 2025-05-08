from flask import abort, make_response
from ..db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response, 400))
    
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))
    
    return model

def create_model(cls, model_data):
    try: 
        new_model = cls.from_dict(model_data)
    except KeyError as error:
        # response = {"message": f"Invalid request: missing {error.args[0]}"}
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_model)
    db.session.commit()

    return {"task": new_model.to_dict()}, 201 # MAKE THIS UNIVERSAL LATER SO IT'S NOT TASK {to.lower(cls.__name__)}?

def get_models_with_filters(cls, filters=None):
    query = db.select(cls)
    filters = dict(filters) # is this okay? I think so
    sort_order = filters.pop("sort", None) # defaults to none if not present -- assuming we want to sort by id if 'sort' isn't given

    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))
    if sort_order == "desc":
        sort_clause = cls.title.desc()
    elif sort_order == "asc":
        sort_clause = cls.title.asc() 
    else:
        sort_clause = cls.id
    models = db.session.scalars(query.order_by(sort_clause))
    return [model.to_dict() for model in models] # if we change the ^ one to remove "task", can do model.to_dict("task") here?
