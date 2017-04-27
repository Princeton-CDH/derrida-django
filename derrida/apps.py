from django.apps import AppConfig

class DerridaConfig(AppConfig):
    name = 'derrida'

    def ready(self):
        import derrida.books.signals
