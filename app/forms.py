from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class UploadNoiseForm(FlaskForm):
    image = FileField('Картинка (png/jpg)', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Только изображения (png, jpg, jpeg)')
    ])
    noise = IntegerField('Уровень шума (0-100)', validators=[
        DataRequired(),
        NumberRange(min=0, max=100)
    ])
    recaptcha = RecaptchaField()   #  Google reCAPTCHA
    submit = SubmitField('Загрузить и зашумить')