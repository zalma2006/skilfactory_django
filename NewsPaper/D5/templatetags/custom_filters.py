from django import template

register = template.Library()

CENSOR = ['Европы', 'изоляции', 'жителей', 'ФИФА', 'Гарри', 'приема']


# подберу слова специально чтобы они были в новостях

@register.filter()
def censor(text):
    for wrd in CENSOR:
        if wrd in text:
            rep_len = '*' * (len(wrd) - 1)
            pref = wrd[0]
            rep = f'{pref}{rep_len}'
            text = text.replace(wrd, rep)
        else:
            continue
    return text
