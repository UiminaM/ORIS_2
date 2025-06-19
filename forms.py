from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from datetime import datetime


class CourseCreateForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Описание', validators=[DataRequired()])
    duration_hours = IntegerField('Длительность (часы)', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Создать')

    def validate_duration_hours(self, field):
        if field.data < 0:
            raise ValidationError('Длительность не может быть меньше 0')


class CourseUpdateForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Описание', validators=[DataRequired()])
    duration_hours = IntegerField('Длительность (часы)', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Обновить')

    def validate_duration_hours(self, field):
        if field.data < 0:
            raise ValidationError('Длительность не может быть меньше 0')


class CourseDeleteForm(FlaskForm):
    submit = SubmitField('Удалить')

