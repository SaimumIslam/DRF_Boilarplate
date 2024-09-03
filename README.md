# DRF_Boilarplate

## Table of Contents

- [Developer Instruction](#developer-instruction)
- [Instruction Tests Writing](#instruction-tests-writing)
- [Project Structure](#project-structure)
- [Project Test Structure](#project-test-structure)
- [Run Command](#run-command)
- [Packages](#packages)

We create this template using:

- [DRF Quick Start](https://www.django-rest-framework.org/tutorial/quickstart/)

## Developer Instruction

- constant variable/data: SNAKE_CASE
- folder/file/variable/function: snake_case
- always write view and api connected with swagger schema

## Instruction Tests Writing

**Note**: You are always welcome to do good changes and refactor.

## Project Structure

- api
  - views: suggest APIView class, function for single operation
  - viewsets: extend base Viewset
  - serializers: extend base ModelSerializer
  - minimal_serializers: extend base ModelMinimalSerializer
  - routers

- core
  - managers
  - querysets
  - utils

- repositories
- services: all service based on models
- helpers: complex service classes.
- utils: functions or static class
- models
- urls
- admin
- apps

#### base
override django configue and settings

#### config
default app and settings


## Project Test Structure

## Run Command

`bash setup.sh` (Run first time to setup django environment only once)

`source venv/bin/activate` (Active virtual_environment, name=venv) 

`python manage.py makemigrations` (Create migrations changes)

`python manage.py migrate` (Apply migrations file into db)

`python manage.py runserver` ( Run django server)

`python manage.py createservicerepository` (create service repository)

## Schema command

` python manage.py spectacular --color --file schema.yml` (Validate schema error)

### Packages

- [Django DOC](https://docs.djangoproject.com/en/5.0/)
- [DRF DOC](https://www.django-rest-framework.org/)
- [Swagger drf-spectator](https://drf-spectacular.readthedocs.io/en/latest/index.html)
- [Celery](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html)
- [Pymysql](https://pypi.org/project/pymysql/)
- [Redis](https://pypi.org/project/redis/)
### Testing Packages


### Notes:
- `@extend_schema`: only in views for drf-spectator.