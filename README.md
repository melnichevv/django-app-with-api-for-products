# Species Sequestration tool back-end application

# Quickstart

# Prerequisites

1. Python 3.7+
2. Docker

# API Setup

You need to have poetry package installed first

### osx / linux / bashonwindows

```shell
curl -sSL https://install.python-poetry.org | python3 -
```

### Windows Powershell

```shell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

Then you can make poetry to install virtual envs into projects' folders, if needed to you:

```shell
poetry config virtualenvs.in-project true
```

Then install all the packages

```shell
poetry install
```

Setting up environment variables:

1. Create .env file root directory
2. Fill it out in conformance with `.env.example`

Before start:

```shell
source .venv/bin/activate
python manage.py migrate
python manage.py loaddata djproducts/fixtures/users.json
```

How to start:
```shell
python manage.py runserver 0.0.0.0:8000
```