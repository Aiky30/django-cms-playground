from django.apps import AppConfig


class HistoryConfig(AppConfig):
    name = 'history'

    def ready(self):
        print("Ready to roll!!")
        import history.signals
