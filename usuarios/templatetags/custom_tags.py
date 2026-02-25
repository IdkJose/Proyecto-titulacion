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


@register.filter
def user_reacted(solicitud, user):
    """
    Filtro para verificar si un usuario ha reaccionado a una solicitud.
    Uso: {% if solicitud|user_reacted:user %}...{% endif %}
    """
    return solicitud.reacciones.filter(usuario=user).exists()
