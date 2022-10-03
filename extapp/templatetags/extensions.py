from django import template

register = template.Library()


def capitalize(input_str):
    return input_str.capitalize()


register.filter('capitalize', capitalize)
