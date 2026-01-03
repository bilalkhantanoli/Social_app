from django import template
from feed.models import Like

register = template.Library()

@register.filter
def is_liked_by(post, user):
    return Like.objects.filter(post=post, user=user).exists()
