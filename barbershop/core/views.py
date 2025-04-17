from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .data import masters, services, orders
import datetime

def landing(request):
    """
    Представление для главной страницы (лендинга)
    """
    # Настраиваем минимальную дату для формы (сегодня)
    today = datetime.date.today()
    min_date = today.strftime('%Y-%m-%d')
    
    # Сортируем заказы по ID в обратном порядке для отображения последних
    sorted_orders = sorted(orders, key=lambda x: x['id'], reverse=True)
    
    context = {
        'min_date': min_date,
        'orders': sorted_orders,
    }
    return render(request, 'landing.html', context)

def thanks(request):
    """
    Представление для страницы благодарности после заявки
    """
    return render(request, 'thanks.html')

def orders_list(request):
    """
    Представление для списка всех заявок
    """
    # В реальном приложении здесь нужна проверка доступа (is_staff)
    # if not request.user.is_staff:
    #     return redirect('landing')
    
    # Сортируем заказы по ID в обратном порядке
    sorted_orders = sorted(orders, key=lambda x: x['id'], reverse=True)
    
    # Считаем количество заявок по статусам
    statuses = {
        'new': sum(1 for o in orders if o['status'] == 'новая'),
        'confirmed': sum(1 for o in orders if o['status'] == 'подтвержденная'),
        'completed': sum(1 for o in orders if o['status'] == 'выполненная'),
        'cancelled': sum(1 for o in orders if o['status'] == 'отмененная'),
    }
    
    context = {
        'orders': sorted_orders,
        'statuses': statuses
    }
    return render(request, 'orders_list.html', context)

def order_detail(request, order_id):
    """
    Представление для деталей конкретной заявки
    """
    # В реальном приложении здесь нужна проверка доступа (is_staff)
    # if not request.user.is_staff:
    #     return redirect('landing')
    
    # Ищем заявку по ID
    order = None
    for o in orders:
        if o['id'] == order_id:
            order = o
            break
    
    if order is None:
        raise Http404("Заявка не найдена")
    
    context = {
        'order': order
    }
    return render(request, 'order_detail.html', context)