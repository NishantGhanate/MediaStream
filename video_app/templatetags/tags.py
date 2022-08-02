from django import template
import datetime

register = template.Library()

@register.filter
def duration(timedelta):
    """
    Format a duration field into HH:MM:SS
    :rtype: str
    """
    total_seconds = int(timedelta.total_seconds())
    time_duration = datetime.timedelta(seconds= total_seconds)

    return f"{time_duration}"
    
@register.filter
def quality(dimension):
    """
    Format resolution dimension to Quality from 1920x1080p to 1080p
    :rtype: str
    """
    height = dimension.split('x')[1]

    return f"{height}p"

@register.filter
def genre(genre_qs):
    name = genre_qs.all()

    return f"{name[0]}"

