"""
Management utility to create service repository.
"""
import os
import sys

from django.core import exceptions
from django.conf import settings
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError


class NotRunningInTTYException(Exception):
    pass


class Command(BaseCommand):
    help = "Used to create service and repository."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = None
        self.app_name = None
        self.APP_MODELS = []
        self.PROJECT_APPS = self._get_installed_project_apps()

    def handle(self, *args, **options):
        try:
            while self.app_name is None:
                app_name = self._get_input_data("app")
                if app_name in self.PROJECT_APPS:
                    self.app_name = app_name
                    self.APP_MODELS = self._get_app_models_by_app(app_name)
                else:
                    self.stdout.write(self.style.ERROR(f'please give one of {",".join(self.PROJECT_APPS)}'))

            while self.model_name is None:
                model_name = self._get_input_data("model")
                if model_name in self.APP_MODELS:
                    self.model_name = model_name
                else:
                    self.stdout.write(self.style.ERROR(f'please give one of {",".join(self.APP_MODELS)}'))

            repository_file_path = self._get_repository_file_path()
            service_file_path = self._get_service_file_path()

            with open(service_file_path, 'w') as file:
                service_file_content = self.get_service_file_template()
                file.write(service_file_content)

            with open(repository_file_path, 'w') as file:
                repository_file_content = self.get_repository_file_template()
                file.write(repository_file_content)

            if options["verbosity"] >= 1:
                self.stdout.write(
                    self.style.SUCCESS(f'Service and repository file created successfully at {self.app_name}'))

        except KeyboardInterrupt:
            self.stderr.write("\nOperation cancelled.")
            sys.exit(1)
        except exceptions.ValidationError as e:
            raise CommandError("; ".join(e.messages))
        except NotRunningInTTYException:
            self.stdout.write(
                "service repository creation skipped due to not running in a TTY. "
                "You can run `manage.py createsuperuser` in your project "
                "to create one manually."
            )

    def _get_input_data(self, category, default=""):
        """Override this method if you want to customize data inputs"""

        input_message = f"Please input {category} name :"
        raw_value = input(input_message)
        if default and raw_value == "":
            raw_value = default
        return raw_value.strip()

    def _get_installed_project_apps(self):
        project_directory = os.getcwd()
        django_app_names = []

        for folder in os.listdir(project_directory):
            folder_path = os.path.join(project_directory, folder)

            app_name = folder

            is_dir = os.path.isdir(folder_path)

            if not is_dir:
                continue

            has_app_file = 'apps.py' in os.listdir(folder_path)
            is_installed_app = app_name in settings.INSTALLED_APPS

            if has_app_file and is_installed_app:
                django_app_names.append(app_name)

        return django_app_names

    def _is_file_exist_in_folder(self, folder, file_name):
        folder_path = os.path.join(folder, f'{file_name}.py')
        return os.path.exists(folder_path)

    def _get_app_models_by_app(self, app_name):
        app_config = apps.get_app_config(app_name)
        service_folder = os.path.join(app_config.path, 'services')
        repository_folder = os.path.join(app_config.path, 'repositories')
        app_models = []

        for model in app_config.get_models():
            model_name = model.__name__

            has_repository = self._is_file_exist_in_folder(repository_folder, model_name)
            has_service = self._is_file_exist_in_folder(service_folder, model_name)
            if has_service or has_repository:
                continue

            app_models.append(model_name)
        return app_models

    def _get_base_file_name(self):
        result = [self.model_name[0].lower()]  # Convert the first character to lowercase
        for char in self.model_name[1:]:
            if char.isupper():
                result.extend(['_', char.lower()])
            else:
                result.append(char)

        return ''.join(result)

    def _get_repository_file_path(self):
        base_file_name = self._get_base_file_name()
        repositories_path = os.path.join(self.app_name, 'repositories')
        os.makedirs(repositories_path, exist_ok=True)
        repository_file_path = os.path.join(repositories_path, f'{base_file_name}.py')

        return repository_file_path

    def _get_service_file_path(self):
        base_file_name = self._get_base_file_name()
        services_path = os.path.join(self.app_name, 'services')
        os.makedirs(services_path, exist_ok=True)
        service_file_path = os.path.join(services_path, f'{base_file_name}.py')

        return service_file_path

    def get_service_file_template(self):
        model_name_snake_case = self._get_base_file_name()

        template = f"""
from base.services.base import BaseService
from {self.app_name}.repositories.{model_name_snake_case} import {self.model_name}Repository


class {self.model_name}Service(BaseService):
    def __init__(self):
        super().__init__({self.model_name}Repository)"""

        return template

    def get_repository_file_template(self):
        template = f"""
from base.repositories.base import BaseRepository
from {self.app_name}.models import {self.model_name}


class {self.model_name}Repository(BaseRepository):
    def __init__(self):
        super().__init__({self.model_name})"""

        return template
