from django import template
from django.forms import BoundField

register = template.Library()

@register.filter(name='add_attrs')
def add_attrs(field, css):
    attrs = {}
    definition = css.split(',')

    for d in definition:
        if '=' in d:
            key, value = d.split('=')
            attrs[key.strip()] = value.strip()

    if isinstance(field, BoundField):
        return field.as_widget(attrs=attrs)
    return field
