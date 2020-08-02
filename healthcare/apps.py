from django.apps import AppConfig


class HealthcareConfig(AppConfig):
    name = 'healthcare'

    def ready(self):
        import healthcare.signals