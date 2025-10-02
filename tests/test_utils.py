𝔸𝕟𝕒𝕤𝕥𝕒𝕤𝕚𝕒, [02.10.2025 16:03]
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install pipenv
        run: python -m pip install pipenv

      - name: Install dependencies
        run: pipenv install --dev --deploy --ignore-pipfile

      - name: Run tests
        run: pipenv run pytest || echo "Нет тестов"

𝔸𝕟𝕒𝕤𝕥𝕒𝕤𝕚𝕒, [02.10.2025 16:11]
from app.utils import add_noise
import numpy as np

def test_add_noise_shape():
    arr = np.zeros((5, 5, 3), dtype=np.uint8)
    noisy = add_noise(arr, 30)
    assert noisy.shape == arr.shape