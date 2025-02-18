from django import template


register = template.Library()


@register.filter
def convert_to_mm_of_mercury(pressure):
    try:
        result = pressure * 0.750062
        return int(result)
    except (ValueError, TypeError):
        return pressure