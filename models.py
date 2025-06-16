from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String, nullable=False)
    author: Mapped[str] = mapped_column(db.String, nullable=True)
    annotation: Mapped[str] = mapped_column(db.String(200))
    year: Mapped[int] = mapped_column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<Book {self.title}>'

def create_table(app: Flask):
    with app.app_context():
        db.create_all()
