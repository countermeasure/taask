import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='inputclass')
def inputclass(field, class_to_add):
    """Allows a class or classes to be added to a form input field."""

    return field.as_widget(attrs={"class":class_to_add})


@register.filter(name='labelclass')
def labelclass(field, class_to_add):
    """Allows a class or classes to be added to a form tag."""

    field_string = unicode(field)
    existing_class_regex = re.compile(r'(?<=class=["\'])(.*?)(?=["\'])')
    match = existing_class_regex.search(field_string)
    if match:
        m = re.search(r'^%s$|^%s\s|\s%s\s|\s%s$' % (class_to_add, class_to_add,
                                                    class_to_add, class_to_add),
                                                    match.group(1))
        print match.group(1)
        if not m:
            return mark_safe(existing_class_regex.sub(match.group(1) + " " +
                             class_to_add, field_string))
    else:
        return mark_safe(field_string.replace('>',
            ' class="%s">' % class_to_add, 1))
    return value


@register.filter(name='autofocus')
def autofocus(field):
    """Sets autofocus for a form input element."""

    field_string = unicode(field)

    return mark_safe(field_string.replace('>', ' autofocus>', 1))
