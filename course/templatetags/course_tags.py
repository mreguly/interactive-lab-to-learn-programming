from django import template

register = template.Library()


@register.filter(name='map_lang')
def map_lang(value):
    int_to_lang = {
        0: "Python",
        1: "C",
        2: "C++",
        3: "Java",
    }
    return int_to_lang.get(value)