from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def chr(value):
    try:
        return __builtins__["chr"](int(value))
    except Exception:
        return ""
