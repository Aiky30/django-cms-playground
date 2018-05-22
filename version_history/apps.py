from django.apps import AppConfig


class VersionHistoryConfig(AppConfig):
    name = 'version_history'

    def ready(self):
        import version_history.signals
