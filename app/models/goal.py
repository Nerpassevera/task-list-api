from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50))
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    # The __init__ method is defined instead of a from_dict class method.
    # Since this model only requires one parameter, from_dict isn't necessary.
    # By defining __init__, the constructor becomes more flexible, allowing
    # both positional and keyword arguments for instantiation.
    def __init__(self, title) -> None:
        self.title = title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }
