from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = "Управление барбершопом"

    def ready(self):
        """
        Импортируем сигналы при загрузке приложения
        """
        try:
            import core.signals
        except ImportError:
            pass
