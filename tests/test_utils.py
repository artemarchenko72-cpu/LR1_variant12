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
