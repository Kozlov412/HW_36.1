from .data import masters, services

def common_context(request):
    """
    Контекстный процессор для добавления общих данных во все шаблоны.
    """
    context = {
        'masters': masters,
        'services': services,
        'is_staff': True,  # Временно для тестирования
    }
    return context