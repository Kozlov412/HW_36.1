from django.shortcuts import render, get_object_or_404
from .data import masters, services, orders


def landing(request):
    """Представление для главной страницы (лендинга)"""
    context = {
        'masters': masters,
        'services': services
    }
    return render(request, 'landing.html', context)

def thanks(request):
    """Представление для страницы благодарности после заявки"""
    return render(request, 'thanks.html')

def orders_list(request):
    """Представление для списка всех заявок"""
    context = {
        'orders': orders
    }
    return render(request, 'orders_list.html', context)

def order_detail(request, order_id):
    """Представление для деталей конкретной заявки"""
    # Имитация get_object_or_404 с нашими тестовыми данными
    order = None
    for o in orders:
        if o['id'] == order_id:
            order = o
            break
    
    # Если заявка не найдена, выдаем 404
    if order is None:
        from django.http import Http404
        raise Http404("Заявка не найдена")
    
    context = {
        'order': order,
        'masters': masters
    }
    return render(request, 'order_detail.html', context)