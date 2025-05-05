from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def replace(request, key, value):
    url_dict = request.GET.copy()
    # print(url_dict)
    # print(url_dict.urlencode())
    url_dict[key] = value
    # print(url_dict.urlencode())
    encode_url =url_dict.urlencode()
    return mark_safe(f"?{encode_url}")