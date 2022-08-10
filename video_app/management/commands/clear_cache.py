from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from django.conf import settings
from django.apps import apps

from video_app import mixins

class Command(BaseCommand):
    """
    Created this command to clear all / model cache 
    e.g python manage.py clear_cache -m VideoModel

    """

    help = 'Takes none / model name in argument'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('-m', '--model', nargs='+', type=str,
            help='To clear cache of speific model'
        )
        
        
    def handle(self, *args, **options):
        models_list = options['model']
        if not models_list:
            cache.clear()
            self.stdout.write(
                self.style.SUCCESS(f'Complete cache cleared')
            )
            return 

        for m in models_list:
            model = self.find_cached_model(model_name= m)
            if not model:
                continue
            
            cache_key = getattr(model, 'CACHE_KEY')
            if not cache_key:
                continue
            keys = cache.keys(f"*{cache_key}*")
            if keys:
                self.stdout.write(self.style.WARNING(
                    f'Found {len(keys)} keys'
                ))
                cache.delete_many(keys)
                self.stdout.write(
                    self.style.SUCCESS(f'Cache cleared !')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'No Cache !')
                )
        return 
        
    def find_cached_model(self, model_name):
        app_model = None
        try :
            model = apps.get_app_config('video_app').get_model(model_name)
            if issubclass(model, mixins.ModelCacheMixin):
                app_model = model
                self.stdout.write(self.style.WARNING(
                    f'\n{app_model}'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'{model} is not subclass of ModelCacheMixin'
                ))
        except LookupError as le:
            self.stdout.write(self.style.ERROR(
                str(le)
            ))
        
        return app_model

            

            