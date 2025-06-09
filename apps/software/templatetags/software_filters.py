# apps/software/templatetags/software_filters.py
from django import template

register = template.Library()

@register.filter
def naira_format(value):
    """Format number as Nigerian Naira with commas"""
    try:
        # Convert to int if it's a string
        if isinstance(value, str):
            value = int(value)
        # Format with commas
        return f"₦{value:,}"
    except (ValueError, TypeError):
        return f"₦{value}"

@register.filter
def lookup(dictionary, key):
    """Template filter to lookup dictionary values"""
    return dictionary.get(key)
