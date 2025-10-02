import os
from flask import Flask, render_template, flash, request
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
from dotenv import load_dotenv

from app.forms import UploadNoiseForm
from app.utils import add_noise, image_to_base64_pil, plot_histogram_base64, resize_image

# Загружаем переменные окружения из .env (локально)
load_dotenv()

# Создаём Flask-приложение
app = Flask(__name__, template_folder='templates', static_folder='static')

# Ключи и настройки
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-me')
app.config['RECAPTCHA_PUBLIC_KEY'] = os.environ.get('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ.get('RECAPTCHA_PRIVATE_KEY')
app.config['WTF_CSRF_ENABLED'] = False

# Ограничение размера загружаемого файла (2 МБ)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

# Папки для загрузки и результатов
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
RESULT_FOLDER = os.path.join(app.root_path, 'static', 'results')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Допустимые расширения
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename: str) -> bool:
    """Проверка допустимого расширения файла"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadNoiseForm()

    if form.validate_on_submit():  # reCAPTCHA проверяется
        f = form.image.data
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            saved_path = os.path.join(UPLOAD_FOLDER, filename)
            f.save(saved_path)

            # Уменьшаем изображение
            pil = resize_image(saved_path, max_size=(800, 800)).convert('RGB')
            arr = np.array(pil)

            # Добавляем шум
            noisy_arr = add_noise(arr, int(form.noise.data))
            noisy_pil = Image.fromarray(noisy_arr)

            # Сохраняем результат
            noisy_fname = f'noisy_{filename}'
            noisy_path = os.path.join(RESULT_FOLDER, noisy_fname)
            noisy_pil.save(noisy_path)

            # Кодируем изображения и гистограммы
            orig_b64 = image_to_base64_pil(pil)
            noisy_b64 = image_to_base64_pil(noisy_pil)
            hist_orig = plot_histogram_base64(arr, title='Исходная')
            hist_noisy = plot_histogram_base64(noisy_arr, title='Зашумлённая')

            return render_template('result.html',
                                   orig_b64=orig_b64,
                                   noisy_b64=noisy_b64,
                                   hist_orig=hist_orig,
                                   hist_noisy=hist_noisy)
        else:
            flash('Файл должен быть png, jpg или jpeg.', 'danger')
    else:
        if request.method == 'POST':  # Отладка: если не прошло
            print("Form errors:", form.errors)
            for field, errs in form.errors.items():
                flash(f"{field}: {'; '.join(errs)}", 'danger')

    return render_template('index.html', form=form)