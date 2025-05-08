from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime
from typing import Optional # dont HAVE to include this, could still be 'null' without it...?

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    # completed_at represents the data a task is completed on -- can be nullable. null value = not completed yet. 
    # When a task is created, completed_at should be null (AKA None) 

    @classmethod
    def from_dict(cls, task_data):
        completed_at = task_data.get("completed_at") # does this work..?
        if completed_at:
            is_complete = True
        else:
            is_complete = False
        new_task = cls(title=task_data["title"],
                       description=task_data["description"],
                    #    is_complete=completed_at is not None # ignore for now, default to null?
        )
        
        return new_task

    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = self.completed_at is not None # does this work?
        # if self.completed_at: # so it's not null 
        #     task_as_dict["completed_at"] = True
        return task_as_dict