from django import template
from feed.models import Like

register = template.Library()

@register.filter
def is_liked_by(post, user):
    return Like.objects.filter(post=post, user=user).exists()

@register.filter
def image_url_check(image_field):
    if not image_field:
        return ""
    try:
        if hasattr(image_field, 'name') and image_field.name and str(image_field.name).startswith(('http://', 'https://')):
            return image_field.name
        return image_field.url
    except Exception:
        return ""
