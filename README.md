# Django products API application

# Quickstart

# Prerequisites

1. Python 3.9+
2. Docker

# API Setup

```shell
docker-compose build
docker-compose up
docker-compose run django python manage.py migrate
docker-compose run django python manage.py loaddata djproducts/fixtures/users.json djproducts/fixtures/products.json
```

Default password for all users is `12asdf34`

## TODO

- Add [django-fsm](https://github.com/viewflow/django-fsm) package for easier tracking order status change;
- Add tests for some basic functionality using `pytest`;
- Add [factory-boy](https://factoryboy.readthedocs.io/en/stable/) for easier products generation
- Play with django-silk and profile API requests in order to speed up API and get rid of excess DB queries (if any :D).