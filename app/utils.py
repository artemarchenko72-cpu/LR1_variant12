import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import io, base64, os

#Уменьшение картинки (чтобы не падало по памяти на Render)
def resize_image(image_path, max_size=(800, 800)):
    img = Image.open(image_path)
    img.thumbnail(max_size)  # сохраняет пропорции
    return img

#Добавление шума
def add_noise(img_array, noise_level):
    noise = np.random.randint(-noise_level, noise_level, img_array.shape, dtype='int16')
    noisy = np.clip(img_array.astype('int16') + noise, 0, 255).astype('uint8')
    return noisy

#Перевод PIL-изображения в base64 для HTML
def image_to_base64_pil(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return "data:image/png;base64," + base64.b64encode(buf.read()).decode('utf-8')

#Построение гистограммы и кодирование в base64
def plot_histogram_base64(img_array, title="Гистограмма") -> str:
    fig, ax = plt.subplots(figsize=(6, 4))

    # Если картинка цветная (3 канала), строим R, G, B
    if len(img_array.shape) == 3 and img_array.shape[2] == 3:
        colors = ('red', 'green', 'blue')
        for i, col in enumerate(colors):
            ax.hist(img_array[:, :, i].ravel(), bins=256, color=col, alpha=0.5, label=col.upper())
        ax.legend()
    else:
        # Ч/б изображение
        ax.hist(img_array.ravel(), bins=256, color='gray', alpha=0.7)

    ax.set_title(title)
    ax.set_xlabel("Pixel value")
    ax.set_ylabel("Frequency")

    buf = io.BytesIO()
    fig.savefig(buf, format="PNG")
    plt.close(fig)  # освобождаем память
    buf.seek(0)
    return "data:image/png;base64," + base64.b64encode(buf.read()).decode('utf-8')