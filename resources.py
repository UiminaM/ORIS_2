from flask_marshmallow import Marshmallow
from flask_restful import Resource
from marshmallow import fields as ma_fields, ValidationError
from models import db, Course
from flask import request, Response
from datetime import datetime
import json

ma = Marshmallow()


class CourseSchema(ma.Schema):
    id = ma_fields.Integer(dump_only=True)
    title = ma_fields.String(required=True)
    description = ma_fields.String(required=True)
    duration_hours = ma_fields.Integer(required=True)


course_schema = CourseSchema()
course_list_schema = CourseSchema(many=True)


class CourseResource(Resource):
    def get(self, course_id):
        query = Course.query.where(Course.id == course_id)
        course = db.session.execute(query).scalar()
        if course:
            data = course_schema.dump(course)
            return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')
        return Response(json.dumps({"error": "Course not found"}, ensure_ascii=False), status=404, mimetype='application/json')

    def patch(self, course_id):
        query = Course.query.where(Course.id == course_id)
        course = db.session.execute(query).scalar()
        if course:
            try:
                if title := request.json.get("title"):
                    course.title = title
                if description := request.json.get("description"):
                    course.description = description
                if duration_hours := request.json.get("duration_hours"):
                    if duration_hours < 0:
                        return Response(json.dumps({"error": "Длительность не может быть меньше 0"}, ensure_ascii=False), status=400, mimetype='application/json')
                    course.duration_hours = duration_hours
                db.session.commit()
                return Response(json.dumps({"message": "Course updated successfully"}, ensure_ascii=False), mimetype='application/json')
            except ValidationError as err:
                return Response(json.dumps({"errors": err.messages}, ensure_ascii=False), status=400, mimetype='application/json')
        return Response(json.dumps({"error": "Course not found"}, ensure_ascii=False), status=404, mimetype='application/json')

    def delete(self, course_id):
        query = Course.query.where(Course.id == course_id)
        course = db.session.execute(query).scalar()
        if course:
            db.session.delete(course)
            db.session.commit()
            return Response(json.dumps({"message": "Course deleted successfully"}, ensure_ascii=False), mimetype='application/json')
        return Response(json.dumps({"error": "Course not found"}, ensure_ascii=False), status=404, mimetype='application/json')


class CourseListResource(Resource):
    def get(self):
        courses = Course.query.all()
        data = course_list_schema.dump(courses)
        return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')

    def post(self):
        data = request.json
        if not data:
            return Response(json.dumps({"error": "No input data provided"}, ensure_ascii=False), status=400, mimetype='application/json')

        try:
            new_course = course_schema.load(data)
        except ValidationError as err:
            return Response(json.dumps({"errors": err.messages}, ensure_ascii=False), status=400, mimetype='application/json')

        course = Course(
            title=new_course['title'],
            description=new_course['description'],
            duration_hours=new_course['duration_hours']
        )
        db.session.add(course)
        db.session.commit()
        return Response(json.dumps(course_schema.dump(course), ensure_ascii=False), status=201, mimetype='application/json')