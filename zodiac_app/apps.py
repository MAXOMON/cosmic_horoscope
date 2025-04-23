from django.apps import AppConfig


class ZodiacAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'zodiac_app'

    def ready(self):
        from django.db.models.signals import post_migrate

        post_migrate.connect(self.start_tasks)
        return super().ready()

    def start_tasks(self, **kwargs):
        from .tasks import update_zodiac_signs, update_weather

        update_zodiac_signs.delay()
        update_weather.delay()
