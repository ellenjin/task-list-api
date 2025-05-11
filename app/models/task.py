from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional, TYPE_CHECKING
from ..db import db
from datetime import datetime
if TYPE_CHECKING:
    from .goal import Goal

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    # completed_at represents the data a task is completed on -- can be nullable. null value = not completed yet. 
    # When a task is created, completed_at should be null (AKA None)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    @classmethod
    def from_dict(cls, task_data):
        completed_at = task_data.get("completed_at")
        if completed_at:
            is_complete = True
        else:
            is_complete = False
        new_task = cls(title=task_data["title"],
                       description=task_data["description"],
                    #    completed_at=task_data["completed_at"] # will this be none if it's not there?
        )
        
        return new_task

    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = self.completed_at is not None

        if self.goal_id:
            task_as_dict["goal_id"] = self.goal_id # Shouldn't affect previous tests
        
        return task_as_dict