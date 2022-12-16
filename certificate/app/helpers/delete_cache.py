from django.core.cache import cache
from django.conf import settings

def del_cache(key_prefix):
    key_pattern = f'views.decorators.cache.cache_*.{key_prefix}.*.{settings.LANGUAGE_CODE}.{settings.TIME_ZONE}'
    print('im here',key_pattern)
    cache.delete_pattern(key_pattern)