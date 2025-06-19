from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from models import db, create_table
from views import CourseView, CourseList, CourseCreate, CourseUpdate, CourseDelete
from resources import CourseResource, CourseListResource
import os

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SECRET_KEY'] = os.urandom(24)
db.init_app(app)

api = Api(app)
migrate = Migrate(app, db)

create_table(app)

app.add_url_rule('/', view_func=CourseList.as_view('course.list', engine=db))
app.add_url_rule('/courses/<int:course_id>/', view_func=CourseView.as_view('course.view', engine=db))
app.add_url_rule('/courses/create/', view_func=CourseCreate.as_view('course.create', engine=db))
app.add_url_rule('/courses/<int:course_id>/update/', view_func=CourseUpdate.as_view('course.update', engine=db))
app.add_url_rule('/courses/<int:course_id>/delete/', view_func=CourseDelete.as_view('course.delete', engine=db))

api.add_resource(CourseListResource, '/api/courses')
api.add_resource(CourseResource, '/api/courses/<int:course_id>')

if __name__ == "__main__":
    app.run(debug=True, port=8000)
