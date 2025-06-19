from flask import request, url_for, render_template, redirect, flash
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy

from forms import CourseDeleteForm, CourseUpdateForm, CourseCreateForm
from models import Course


class CourseList(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self):
        courses: list[Course] = self.engine.session.execute(Course.query).scalars()
        return render_template('course/list.html', courses=courses)


class CourseView(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self, course_id: int):
        query = Course.query.where(Course.id == course_id)
        course: Course = self.engine.session.execute(query).scalar()
        if not course:
            return 'Не найдено'
        return render_template('course/read.html', course=course)


class CourseUpdate(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self, course_id: int):
        query = Course.query.where(Course.id == course_id)
        course: Course = self.engine.session.execute(query).scalar()
        if not course:
            return 'Не найдено'
        form = CourseUpdateForm(
            title=course.title,
            description=course.description,
            duration_hours=course.duration_hours
        )
        return render_template('course/update.html', course=course, form=form)

    def post(self, course_id: int):
        query = Course.query.where(Course.id == course_id)
        course: Course = self.engine.session.execute(query).scalar()
        if not course:
            return 'Не найдено'

        form = CourseUpdateForm(request.form)
        if form.validate():
            course.title = form.title.data
            course.description = form.description.data
            course.duration_hours = form.duration_hours.data
            self.engine.session.commit()
            flash('Курс успешно обновлен!', 'success')

        return redirect(url_for('course.list'))


class CourseDelete(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self, course_id: int):
        query = Course.query.where(Course.id == course_id)
        course: Course = self.engine.session.execute(query).scalar()
        if not course:
            return 'Не найдено'
        form = CourseDeleteForm()
        return render_template('course/delete.html', course=course, form=form)

    def post(self, course_id: int):
        query = Course.query.where(Course.id == course_id)
        course: Course = self.engine.session.execute(query).scalar()
        if not course:
            return 'Не найдено'
        form = CourseDeleteForm(request.form)
        if form.validate():
            self.engine.session.delete(course)
            self.engine.session.commit()
            flash('Курс успешно удален!', 'success')

        return redirect(url_for('course.list'))


class CourseCreate(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self):
        form = CourseCreateForm()
        return render_template('course/create.html', form=form)

    def post(self):
        form = CourseCreateForm(request.form)
        if form.validate():
            try:
                course = Course(
                    title=form.title.data,
                    description=form.description.data,
                    duration_hours=form.duration_hours.data
                )
                self.engine.session.add(course)
                self.engine.session.commit()
                flash('Курс успешно создан!', 'success')
                return redirect(url_for('course.list'))
            except Exception as e:
                self.engine.session.rollback()
                flash(f'Ошибка при создании курса: {str(e)}', 'error')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{getattr(form, field).label.text}: {error}', 'error')
        return render_template('course/create.html', form=form)
