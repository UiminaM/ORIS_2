from flask_marshmallow import Marshmallow
from flask_restful import Resource
from marshmallow import Schema, fields as ma_fields, ValidationError
from models import db, Book
from flask import request, jsonify
from datetime import datetime

ma = Marshmallow()


class BookSchema(ma.Schema):
    id = ma_fields.Integer(dump_only=True)
    title = ma_fields.String(required=True)
    author = ma_fields.String(required=True)
    annotation = ma_fields.String(required=True)
    year = ma_fields.Integer(required=True)
    


book_schema = BookSchema()
book_list_schema = BookSchema(many=True)


class BookResource(Resource):
    def get(self, book_id):
        query = Book.query.where(Book.id == book_id)
        book = db.session.execute(query).scalar()
        if book:
            return book_schema.dump(book)
        return {"error": "Book not found"}, 404

    def patch(self, book_id):
        query = Book.query.where(Book.id == book_id)
        book = db.session.execute(query).scalar()
        if book:
            try:
                if title := request.json.get("title"):
                    book.title = title
                if year := request.json.get("year"):
                    current_year = datetime.now().year
                    if year > current_year:
                        return {"error": "Год не может быть больше текущего"}, 400
                    if len(str(year)) > 4:
                        return {"error": "Год не может содержать более 4 цифр"}, 400
                    book.year = year
                if author := request.json.get("author"):
                    book.author = author
                if annotation := request.json.get("annotation"):
                    book.annotation = annotation
                db.session.commit()
                return {"message": "Book updated successfully"}
            except ValidationError as err:
                return {"errors": err.messages}, 400
        return {"error": "Book not found"}, 404

    def delete(self, book_id):
        query = Book.query.where(Book.id == book_id)
        book = db.session.execute(query).scalar()
        if book:
            db.session.delete(book)
            db.session.commit()
            return {"message": "Book deleted successfully"}
        return {"error": "Book not found"}, 404


class BookListResource(Resource):
    def get(self):
        books = Book.query.all()
        return book_list_schema.dump(books)

    def post(self):
        data = request.json
        if not data:
            return {"error": "No input data provided"}, 400

        try:
            new_book = book_schema.load(data)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        book = Book(
            title=new_book['title'],
            author=new_book['author'],
            annotation=new_book['annotation'],
            year=new_book['year']
        )
        db.session.add(book)
        db.session.commit()
        return book_schema.dump(book), 201


