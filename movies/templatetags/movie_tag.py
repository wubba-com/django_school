from django import template
from django_movies.movies.models import Category

register = template.library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()
