import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')   # обязательно для серверного рендера графиков
import matplotlib.pyplot as plt
import io
import base64

def add_noise(img_arr: np.ndarray, noise_percent: int) -> np.ndarray:
    """
    Добавляет равномерный (uniform) шум:
    noise_percent: 0..100 — доля максимального смещения (255 * frac)
    """
    frac = max(0.0, min(100.0, float(noise_percent))) / 100.0
    # шум в диапазоне [-0.5, +0.5] * 255 * frac
    noise = (np.random.rand(*img_arr.shape) - 0.5) * 255.0 * frac
    out = img_arr.astype(np.float32) + noise
    out = np.clip(out, 0, 255).astype(np.uint8)
    return out

def image_to_base64_pil(img_pil: Image.Image) -> str:
    buf = io.BytesIO()
    img_pil.save(buf, format='PNG')
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('ascii')

def plot_histogram_base64(img_arr: np.ndarray, title: str='') -> str:
    """
    Строит на одном графике кривые распределения для R, G, B и возвращает base64 PNG.
    """
    fig = plt.figure(figsize=(6,3))
    ax = fig.add_subplot(1,1,1)
    colors = ('r', 'g', 'b')
    for i, c in enumerate(colors):
        hist, bins = np.histogram(img_arr[:,:,i].flatten(), bins=256, range=(0,255))
        ax.plot(hist, label=c)
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('ascii')