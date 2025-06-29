from django import template

register = template.Library()

@register.filter(name="add_class")
def add_class(field, css_classes):
    """
    Django template filter to add CSS classes to a form field widget,
    merging with any existing classes.
    Usage in template: {{ field|add_class:"class1 class2" }}
    """
    existing_classes = field.field.widget.attrs.get("class", "")
    classes = f"{existing_classes} {css_classes}".strip() if existing_classes else css_classes
    return field.as_widget(attrs={"class": classes})