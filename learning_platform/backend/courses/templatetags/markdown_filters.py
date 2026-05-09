import markdown
import bleach

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def markdown_to_html(value):
    if not value:
        return ""

    html = markdown.markdown(
        value,
        extensions=[
            "extra",
            "nl2br",
            "sane_lists",
        ]
    )

    allowed_tags = [
        "p", "br",
        "strong", "em", "b", "i",
        "h1", "h2", "h3", "h4",
        "ul", "ol", "li",
        "blockquote",
        "code", "pre",
        "a",
        "hr"
    ]

    allowed_attrs = {
        "a": ["href", "title", "target", "rel"]
    }

    clean_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True
    )

    return mark_safe(clean_html)