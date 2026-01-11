from django import template

register = template.Library()

@register.filter
def get_dict(dictionary, key):
    """
    Filtro personalizado para obtener valores de un diccionario en templates.
    Uso: {{ diccionario|get_dict:clave }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
