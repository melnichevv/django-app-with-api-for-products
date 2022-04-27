# Django products API application

# Quickstart

# Prerequisites

1. Python 3.9+
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
cd api
poetry install
```

Setting up environment variables:

1. Create .env file in directory
2. Fill it out in conformance with `.env.example`

Before start:

```shell
docker-compose build
docker-compose up
docker-compose run django python manage.py migrate
docker-compose run django python manage.py loaddata djproducts/fixtures/users.json djproducts/fixtures/products.json
```