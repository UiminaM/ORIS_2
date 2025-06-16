from flask import request, url_for, render_template, redirect, flash
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy

from forms import BookDeleteForm, BookUpdateForm, BookCreateForm
from models import Book


class BookList(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self):
        books: list[Book] = self.engine.session.execute(Book.query).scalars()
        return render_template('book/list.html', books=books)


class BookView(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self, book_id: int):
        query = Book.query.where(Book.id == book_id)
        book: Book = self.engine.session.execute(query).scalar()
        if not book:
            return 'Не найдено'
        return render_template('book/read.html', book=book)


class BookUpdate(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self, book_id: int):
        query = Book.query.where(Book.id == book_id)
        book: Book = self.engine.session.execute(query).scalar()
        if not book:
            return 'Не найдено'
        form = BookUpdateForm(
            title=book.title,
            annotation=book.annotation,
            year=book.year
        )
        return render_template('book/update.html', book=book, form=form)

    def post(self, book_id: int):
        query = Book.query.where(Book.id == book_id)
        book: Book = self.engine.session.execute(query).scalar()
        if not book:
            return 'Не найдено'

        form = BookUpdateForm(request.form)
        if form.validate():
            book.title = form.title.data
            book.annotation = form.annotation.data
            book.year = form.year.data
            self.engine.session.commit()
            flash('Книга успешно обновлена!', 'success')

        return redirect(url_for('book.list'))


class BookDelete(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self, book_id: int):
        query = Book.query.where(Book.id == book_id)
        book: Book = self.engine.session.execute(query).scalar()
        if not book:
            return 'Не найдено'
        form = BookDeleteForm()
        return render_template('book/delete.html', book=book, form=form)

    def post(self, book_id: int):
        query = Book.query.where(Book.id == book_id)
        book: Book = self.engine.session.execute(query).scalar()
        if not book:
            return 'Не найдено'
        form = BookDeleteForm(request.form)
        if form.validate():
            self.engine.session.delete(book)
            self.engine.session.commit()
            flash('Книга успешно удалена!', 'success')

        return redirect(url_for('book.list'))


class BookCreate(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self):
        form = BookCreateForm()
        return render_template('book/create.html', form=form)

    def post(self):
        form = BookCreateForm(request.form)
        if form.validate():
            try:
                book = Book(
                    title=form.title.data,
                    annotation=form.annotation.data,
                    year=form.year.data
                )
                self.engine.session.add(book)
                self.engine.session.commit()
                flash('Книга успешно создана!', 'success')
                return redirect(url_for('book.list'))
            except Exception as e:
                self.engine.session.rollback()
                flash(f'Ошибка при создании книги: {str(e)}', 'error')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{getattr(form, field).label.text}: {error}', 'error')
        return render_template('book/create.html', form=form)
