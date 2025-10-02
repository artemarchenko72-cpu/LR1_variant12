import os
import random
from flask import Flask, render_template, flash, session
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

from app.forms import UploadNoiseForm
from app.utils import add_noise, image_to_base64_pil, plot_histogram_base64

app = Flask(__name__, template_folder='templates', static_folder='static')
# настройка секретного ключа (в PyCharm зададим в Run Configuration)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-me')

# Папки для сохранения загруженных и результатных изображений
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
RESULT_FOLDER = os.path.join(app.root_path, 'static', 'results')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadNoiseForm()

    # На GET (и при первой загрузке) генерируем простую математическую капчу и сохраняем ответ в session
    if 'captcha_answer' not in session or (form is None):
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        session['captcha_question'] = f"{a} + {b} = ?"
        session['captcha_answer'] = a + b

    if form.validate_on_submit():
        # проверка капчи
        try:
            user_ans = int(form.captcha.data)
        except Exception:
            flash('Капча должна быть целым числом.', 'danger')
            return render_template('index.html', form=form, captcha_question=session.get('captcha_question'))

        if user_ans != session.get('captcha_answer'):
            flash('Неверный ответ на капчу. Попробуйте снова.', 'danger')
            # заново сгенерируем капчу:
            a = random.randint(1, 9)
            b = random.randint(1, 9)
            session['captcha_question'] = f"{a} + {b} = ?"
            session['captcha_answer'] = a + b
            return render_template('index.html', form=form, captcha_question=session.get('captcha_question'))

        f = form.image.data
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            saved_path = os.path.join(UPLOAD_FOLDER, filename)
            f.save(saved_path)

            # Открываем картинку, конвертируем в RGB и numpy
            pil = Image.open(saved_path).convert('RGB')
            arr = np.array(pil)

            # Добавляем шум
            noisy_arr = add_noise(arr, int(form.noise.data))
            noisy_pil = Image.fromarray(noisy_arr)

            # Сохраняем результат
            noisy_fname = f'noisy_{filename}'
            noisy_path = os.path.join(RESULT_FOLDER, noisy_fname)
            noisy_pil.save(noisy_path)

            # Переводим изображения и гистограммы в base64 для вставки в HTML
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
            flash('Неверный файл — допустимы: png, jpg, jpeg.', 'danger')

    # Если не POST или валидация не прошла — показываем форму
    # При каждом рендере показываем актуальную капчу (session['captcha_question'])
    return render_template('index.html', form=form, captcha_question=session.get('captcha_question'))