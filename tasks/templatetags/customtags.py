import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='inputclass')
def inputclass(field, class_to_add):
    """Allows a class or classes to be added to a form input field."""

    return field.as_widget(attrs={"class": class_to_add})


@register.filter(name='labelclass')
def labelclass(field, class_to_add):
    """Allows a class or classes to be added to a form tag."""

    field_string = unicode(field)
    existing_class_regex = re.compile(r'''(?<=class=["'])(.*?)(?=["'])''')
    match = existing_class_regex.search(field_string)
    if match:
        m = re.search(r'^%s$|^%s\s|\s%s\s|\s%s$' % (
            class_to_add,
            class_to_add,
            class_to_add,
            class_to_add
            ), match.group(1))
        if not m:
            field_string = existing_class_regex.sub(
                match.group(1) + " " + class_to_add,
                field_string
            )
    else:
        field_string = field_string.replace('>', ' class="%s">' % class_to_add, 1)
    return mark_safe(field_string)


@register.filter(name='autofocus')
def autofocus(field):
    """Sets autofocus for a form input element."""

    field_string = unicode(field)

    return mark_safe(field_string.replace('>', ' autofocus>', 1))


@register.filter(name='spellcheck')
def spellcheck(field):
    """Sets spellcheck for a form input element."""

    field_string = unicode(field)

    return mark_safe(field_string.replace('>', ' spellcheck="true">', 1))


@register.filter(name='rows')
def rows(field, rows):
    """Allows the number of rows of a TextField to be set.
    Must not be used before the 'inputclass' custom tag.
    """
    field_string = re.sub('rows="\d+"', 'rows="%s"' % rows, unicode(field))

    return mark_safe(field_string)


@register.filter(name='cols')
def cols(field, cols):
    """Allows the number of columns of a TextField to be set.
    Must not be used before the 'inputclass' custom tag.
    """
    field_string = re.sub('cols="\d+"', 'cols="%s"' % cols, unicode(field))

    return mark_safe(field_string)
