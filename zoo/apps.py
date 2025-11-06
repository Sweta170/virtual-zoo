from django.apps import AppConfig


class ZooConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'zoo'

    def ready(self):
        # import signals
        try:
            import zoo.signals  # noqa
        except ImportError:
            pass
