from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class UploadNoiseForm(FlaskForm):
    image = FileField('Картинка (png/jpg)', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Только изображения (png,jpg,jpeg)')
    ])
    noise = IntegerField('Уровень шума (0-100)', validators=[
        DataRequired(),
        NumberRange(min=0, max=100)
    ])
    # Капча — поле для ввода ответа (в самом шаблоне мы покажем текст задачи)
    captcha = IntegerField('Капча — введите ответ', validators=[DataRequired()])
    submit = SubmitField('Загрузить и зашумить')