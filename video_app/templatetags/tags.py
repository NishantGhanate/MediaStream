from django import template
import datetime

register = template.Library()

@register.filter
def duration(timedelta):
    """
    Format a duration field
    :rtype: str
    """
    total_seconds = int(timedelta.total_seconds())
    time_duration = datetime.timedelta(seconds= total_seconds)

    return f"{time_duration}"
    
@register.filter
def quality(dimension):
    """
    Format resolution dimension to Quality
    :rtype: str
    """
    height = dimension.split('x')[1]

    return f"{height}p"
    