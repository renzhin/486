from django.apps import AppConfig


class CpusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cpus'
    verbose_name = 'Процессоры'

    def ready(self):
        import cpus.signals
