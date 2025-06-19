from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Date, Table
from typing import List
from flask import Flask
import datetime


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


class Course(db.Model):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(100), nullable=False)
    description: Mapped[str] = mapped_column(db.Text)
    duration_hours: Mapped[int] = mapped_column(nullable=False)

    
    certificate: Mapped["CourseCertificate"] = relationship(back_populates="course", uselist=False)
   
    lessons: Mapped[List["Lesson"]] = relationship(back_populates="course", cascade="all, delete")

    students: Mapped[List["Student"]] = relationship(
        secondary="student_course",
        back_populates="courses"
    )

    def __repr__(self):
        return f"<Course {self.title}>"


class CourseCertificate(db.Model):
    __tablename__ = "course_certificate"
    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), unique=True)
    template_file: Mapped[str] = mapped_column(db.String(255))
    issue_date: Mapped[datetime.date] = mapped_column(db.Date)

    course: Mapped["Course"] = relationship(back_populates="certificate")


class Lesson(db.Model):
    __tablename__ = "lessons"
    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    title: Mapped[str] = mapped_column(db.String(100), nullable=False)
    content: Mapped[str] = mapped_column(db.Text)

    course: Mapped["Course"] = relationship(back_populates="lessons")


student_course = Table(
    "student_course",
    db.metadata,
    db.Column("student_id", db.ForeignKey("students.id"), primary_key=True),
    db.Column("course_id", db.ForeignKey("courses.id"), primary_key=True)
)


class Student(db.Model):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)

    courses: Mapped[List["Course"]] = relationship(
        secondary=student_course,
        back_populates="students"
    )

    def __repr__(self):
        return f"<Student {self.name}>"


def create_table(app: Flask):
    with app.app_context():
        db.create_all()
