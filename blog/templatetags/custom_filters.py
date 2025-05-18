from django import template
register = template.Library()

@register.filter
def linebreak_every_n_chars(value, n=15):
    n = int(n)
    return '<br>'.join([value[i:i+n] for i in range(0, len(value), n)])