from django.core.cache import cache

def clear_cache(model_instance):
    cache_key = getattr(model_instance, 'CACHE_KEY')
    if not cache_key:
        return 0

    keys = cache.keys(f"*{cache_key}*")
    keys_len = len(keys)
    if keys:
        print(f'Found {keys_len} keys')
        cache.delete_many(keys)
        print(f'Cache cleared for {cache_key}!')
    else:
        print('No Cache !')
    
    return keys_len