from django.apps import AppConfig
import os


class ApiConfig(AppConfig):

    name = "api"

    def ready(self):

        # evitar duplicar thread com autoreload
        if os.environ.get("RUN_MAIN") != "true":
            return

        from api.world.world_simulation import start_world

        start_world()
