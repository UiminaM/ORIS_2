from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from datetime import datetime


class BookCreateForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(min=1, max=100)])
    annotation = TextAreaField('Аннотация', validators=[DataRequired()])
    year = IntegerField('Год издания', validators=[DataRequired()])
    submit = SubmitField('Создать')

    def validate_year(self, year):
        current_year = datetime.now().year
        if year.data > current_year:
            raise ValidationError('Год не может быть больше текущего')
        if len(str(year.data)) > 4:
            raise ValidationError('Год не может содержать более 4 цифр')


class BookUpdateForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(min=1, max=100)])
    annotation = TextAreaField('Аннотация', validators=[DataRequired()])
    year = IntegerField('Год издания', validators=[DataRequired()])
    submit = SubmitField('Обновить')

    def validate_year(self, year):
        current_year = datetime.now().year
        if year.data > current_year:
            raise ValidationError('Год не может быть больше текущего')
        if len(str(year.data)) > 4:
            raise ValidationError('Год не может содержать более 4 цифр')


class BookDeleteForm(FlaskForm):
    submit = SubmitField('Удалить')

