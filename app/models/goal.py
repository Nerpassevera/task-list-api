from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }
