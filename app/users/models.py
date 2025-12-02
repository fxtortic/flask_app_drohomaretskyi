from __future__ import annotations

from datetime import datetime

from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin

from app import db, bcrypt


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str | None] = mapped_column(String(120), unique=True)

    image: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
        default="profile_default.jpg",
    )

    about_me: Mapped[str | None] = mapped_column(Text, nullable=True)

    last_seen: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    password_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="author",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User {self.id} '{self.username}'>"

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        if self.password_hash is None:
            return False
        return bcrypt.check_password_hash(self.password_hash, password)
