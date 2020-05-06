from django import template
register = template.Library()

@register.filter
def hidden_fields(value):
    fields = ['id', 'created', 'updated']
    if value.lower() in fields:
        return True
    else:
        return False
