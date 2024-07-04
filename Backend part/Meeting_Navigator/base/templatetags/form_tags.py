from django import template

register = template.Library()


@register.filter(name='attr')
def attr(field, args):
    # args should be in the form 'attribute_name:attribute_value'
    attrs = {}
    for arg in args.split(','):
        key, value = arg.split(':')
        attrs[key] = value

    return field.as_widget(attrs=attrs)
