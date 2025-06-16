from flask import Flask
from flask_migrate import Migrate
from models import db, create_table
from views import BookView, BookList, BookCreate, BookUpdate, BookDelete
import os

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SECRET_KEY'] = os.urandom(24)
db.init_app(app)

migrate = Migrate(app, db)

create_table(app)

app.add_url_rule('/', view_func=BookList.as_view('book.list', engine=db))
app.add_url_rule('/books/<int:book_id>/', view_func=BookView.as_view('book.view', engine=db))
app.add_url_rule('/books/create/', view_func=BookCreate.as_view('book.create', engine=db))
app.add_url_rule('/books/<int:book_id>/update/', view_func=BookUpdate.as_view('book.update', engine=db))
app.add_url_rule('/books/<int:book_id>/delete/', view_func=BookDelete.as_view('book.delete', engine=db))

if __name__ == "__main__":
    app.run(debug=True)
