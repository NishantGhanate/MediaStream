from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class ModelCacheMixin:
    """
    Mixin for models that adds filtering on cached queryset.

    @required params:
        CACHE_KEY : str : - key name used for caching the queryset
             
        CACHED_RELATED_OBJECT:
            : list - list of foreign key attributes for model that needs to be cached

    """

    @classmethod
    def cache_all(cls):
        """
        Returns stored instances stored in cache
        :return: List of Model instances.
        """
        if not cls.CACHE_KEY:
            raise AttributeError(
                "CACHE_KEY must be defined in {}".format(cls.__name__)
            )

        if cls.CACHED_RELATED_OBJECT:
            queryset = cache.get_or_set(
                cls.CACHE_KEY,
                cls.objects.all().select_related(*cls.CACHED_RELATED_OBJECT),
                timeout=CACHE_TTL
            )
        else:
            queryset = cache.get_or_set(
                cls.CACHE_KEY, cls.objects.all(), timeout=CACHE_TTL
            )
        return queryset

    @classmethod
    def filter_cache(cls, queryset=None, **kwargs):
        """
        Fiter the queryset 
        """
        cached_qs = cls.cache_all()
        if queryset:
            filter_qs = cached_qs.filter(queryset)
        else:
            filter_qs = cached_qs.filter(**kwargs)
        
        return filter_qs

    @classmethod
    def filter_related_cache(cls, queryset=None, **kwargs):
        """
        Filtering is based on model's foreign keys,
        which is set as CACHED_RELATED_OBJECT in model class.
        It currently supports 2 types of filter
        1. Equality Filter for foreign key's table- e.g id = 1 and name = 'test'
           filter_related_cache(foreign_key= {"name": "test", "id": 5})
        2. In List Filter for foreign key's table- e.g id in [1,2,3]
           filter_related_cache(foreign_key={'id': [1,2,3]})
        :param queryset: list of model instances that needs to be filtered.
        :param kwargs: dictionary containing filter property and values.
        :return: List containing Model objects
        """
        if not queryset:
            queryset = cls.cache_all()

        for foreign_key, related_filters in kwargs.items():
            related_objects_list = [getattr(obj, foreign_key) for obj in queryset]
            # Filtering related objects based related object's attribute filtes
            filtered_related_objects = cls.filter_cache(
                related_objects_list, **related_filters
            )
            # Filtering queryset based filtered related objects
            queryset = list(
                filter(
                    lambda x: getattr(x, foreign_key) in filtered_related_objects,
                    queryset,
                )
            )
        return queryset