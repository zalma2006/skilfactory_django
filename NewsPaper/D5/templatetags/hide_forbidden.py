from django import template

register = template.Library()

forbidden_words = [
    'Привет', "надо", "ещё", "поискать", "слова", "для", "замены", "бесконечной", "сталкиваются"]


@register.filter
def hide_forbidden(val):
    words = val.split()
    res = []
    for word in words:
        if word in forbidden_words:
            res.append(word[0] + "*" * (len(word) - 2) + word[-1])
        else:
            res.append(word)
    return ' '.join(res)
