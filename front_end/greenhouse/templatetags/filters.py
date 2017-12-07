from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter(name='percent')
def percent(value, arg):
    return round((value * 100) / arg, 2)


@register.filter(name='underscored')
@stringfilter
def underscored(value):
    return value.replace(' ', '_')


@register.filter(name='seconds_to_time')
def seconds_to_time(value):
    days = int(value) // (60 * 60 * 24)
    hours = (int(value) // (60 * 60)) % 24
    minutes = (int(value) // 60) % 60
    seconds = int(value) % 60
    return '{days} Days, {hours} Hours, {minutes} Minutes, {seconds} Seconds'.format(
        days=days, hours=hours, minutes=minutes, seconds=seconds)


@register.filter(name='sub')
def sub(value, arg):
    return value - arg