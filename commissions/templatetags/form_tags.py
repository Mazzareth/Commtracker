from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """Django template filter to add a CSS class to a form field's widget."""
    widget = field.field.widget
    existing = widget.attrs.get('class', '')
    if existing:
        classes = f"{existing} {css_class}"
    else:
        classes = css_class
    return field.as_widget(attrs={**widget.attrs, 'class': classes})