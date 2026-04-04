from django import template

register = template.Library()


@register.filter
def get_severity_class(severity):
    """Map severity to Bootstrap alert class."""
    mapping = {
        'info': 'alert-info',
        'warning': 'alert-warning',
        'success': 'alert-success',
        'danger': 'alert-danger',
    }
    return mapping.get(severity, 'alert-secondary')


@register.filter
def get_severity_icon(severity):
    """Map severity to Bootstrap icon."""
    mapping = {
        'info': 'bi-info-circle-fill',
        'warning': 'bi-exclamation-triangle-fill',
        'success': 'bi-check-circle-fill',
        'danger': 'bi-x-octagon-fill',
    }
    return mapping.get(severity, 'bi-bell-fill')


@register.filter
def get_priority_class(priority):
    """Map task priority to badge class."""
    mapping = {
        'low': 'bg-secondary',
        'medium': 'bg-info',
        'high': 'bg-warning text-dark',
        'urgent': 'bg-danger',
    }
    return mapping.get(priority, 'bg-secondary')


@register.filter
def get_category_icon(category):
    """Map suggestion category to icon."""
    mapping = {
        'focus': 'bi-bullseye',
        'distraction': 'bi-shield-exclamation',
        'habit': 'bi-calendar-check',
        'task': 'bi-list-task',
        'schedule': 'bi-clock-history',
        'wellness': 'bi-heart-pulse',
    }
    return mapping.get(category, 'bi-lightbulb')


@register.filter
def get_category_color(category):
    """Map suggestion category to color."""
    mapping = {
        'focus': '#6c5ce7',
        'distraction': '#e17055',
        'habit': '#00b894',
        'task': '#0984e3',
        'schedule': '#fdcb6e',
        'wellness': '#e84393',
    }
    return mapping.get(category, '#636e72')


@register.filter
def multiply(value, arg):
    """Multiply a value."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def percentage_of(value, total):
    """Calculate percentage."""
    try:
        return round(float(value) / float(total) * 100) if float(total) > 0 else 0
    except (ValueError, TypeError, ZeroDivisionError):
        return 0
