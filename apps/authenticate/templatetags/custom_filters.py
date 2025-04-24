from django import template

register = template.Library()


@register.filter
def split(value, arg):
    """
    Split a string by a delimiter.
    Example usage: {{ value|split:"delimiter" }}
    """
    return value.split(arg)
