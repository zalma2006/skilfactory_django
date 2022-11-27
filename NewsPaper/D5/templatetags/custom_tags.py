from datetime import datetime

from django import template

register = template.Library()


@register.simple_tag()
def current_time(format_string='%b %d %Y'):
    cur_time = datetime.utcnow().strftime(format_string)
    return f"{cur_time}"
