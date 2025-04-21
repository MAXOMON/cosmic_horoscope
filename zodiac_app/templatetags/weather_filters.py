from django import template


register = template.Library()


@register.filter
def convert_to_mm_of_mercury(pressure):
    try:
        result = pressure * 0.750062
        return "\U0001F321" + " " + str(int(result)) + " мм.рт. "
    except (ValueError, TypeError):
        return pressure

@register.filter
def convert_to_degrees_of_temperature(val: float) -> str:
    try:
        val = str(int(val))
        return f"{val}" + "\U00002103"
    except (ValueError, TypeError):
        return val
    
@register.filter
def to_humidity(val: int) -> str:
    try:
        return "\U0001F4A7" + " " + str(val) + "%"
    except (ValueError, TypeError):
        return val

@register.filter
def to_wind_speed(val: int) -> str:
    try:
        return "\U0001F32B" + " " + str(val) + " м/с "
    except (ValueError, TypeError):
        return val
    
@register.filter
def to_wind_description(val: int) -> str:
    if val == 0 | val == 360:
        return "Северный"
    elif 1 < val < 90:
        return "Cеверо-Восточный"
    elif val == 90:
        return "Восточный"
    elif 90 < val < 180:
        return "Юго-Восточный"
    elif val == 180:
        return "Южный"
    elif 180 < val < 270:
        return "Юго-Западный"
    elif val == 270:
        return "Западный"
    elif 270 < val < 360:
        return "Северо-Западный"
    else:
        return val
        