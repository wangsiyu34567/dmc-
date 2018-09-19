from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class DmcConfig(AppConfig):
    name = 'dmc'

    def ready(self):
        autodiscover_modules('dmc')
