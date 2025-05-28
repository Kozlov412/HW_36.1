from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.urls import reverse
from django.db import transaction
from django.conf import settings
from .models import Order
from barbershop.utils.telegram_bot import send_message
import logging

# Настройка логирования для сигналов
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Order)
def notification_on_order_create(sender, instance, created, **kwargs):
    """
    Сигнал отмечает вновь созданные заказы для последующего уведомления.
    """
    if created:
        # Когда заказ только создан, сбрасываем флаг notification_sent
        if instance.notification_sent:
            instance.notification_sent = False
            instance.save(update_fields=['notification_sent'])
        logger.info(f"Создан новый заказ #{instance.id}, ожидается добавление услуг")

@receiver(m2m_changed, sender=Order.services.through)
def notification_on_services_added(sender, instance, action, pk_set, **kwargs):
    """
    Сигнал срабатывает при добавлении услуг к заказу.
    Отправляет уведомление со списком выбранных услуг.
    """
    # Если услуги успешно добавлены к заказу и уведомление ещё не было отправлено
    if action == 'post_add' and not instance.notification_sent:
        logger.info(f"Добавлены услуги к заказу #{instance.id}, подготовка уведомления")
        
        try:
            # Получаем список услуг
            services = instance.services.all()
            
            # Если список услуг пуст, не отправляем уведомление
            if not services.exists():
                logger.warn(f"К заказу #{instance.id} не добавлено ни одной услуги, уведомление не отправлено")
                return
            
            # Формируем список услуг в читаемом формате
            services_list = "\n".join([f"• {service.name} - {service.price} руб." 
                                     for service in services])
            
            # Вычисляем общую сумму
            total_sum = sum([service.price for service in services])
            
            # Формируем полное сообщение со всеми деталями заказа
            message = (
                f"*📱 НОВАЯ ЗАЯВКА #{instance.id}*\n\n"
                f"*Клиент:* {instance.client_name}\n"  # Используем client_name вместо name
                f"*Телефон:* {instance.phone}\n"
            )
            
            # Добавляем дату и время записи
            if instance.appointment_date:
                date_str = instance.appointment_date.strftime('%d.%m.%Y')
                time_str = instance.appointment_date.strftime('%H:%M')
                message += f"*Дата записи:* {date_str}\n"
                message += f"*Время записи:* {time_str}\n"
            
            # Добавляем информацию о мастере, если он назначен
            if instance.master:
                message += f"*Мастер:* {instance.master}\n"
                
            # Добавляем комментарий, если он есть
            if instance.comment:
                message += f"*Комментарий:* {instance.comment}\n"
            else:
                message += "*Комментарий:* Отсутствует\n"
                
            # Добавляем список услуг и сумму
            message += f"\n*Выбранные услуги:*\n{services_list}\n\n"
            message += f"*Общая сумма:* {total_sum} руб.\n\n"
            
            # Добавляем ссылку на административный интерфейс для просмотра заказа
            base_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
            admin_url = f"{base_url}/admin/core/order/{instance.id}/change/"
            message += f"[Открыть заявку в админке]({admin_url})"
            
            # Отправляем сообщение в транзакции
            def send_and_update():
                # Отправляем сообщение
                send_message(message)
                
                # Обновляем флаг отправки уведомления
                Order.objects.filter(id=instance.id).update(notification_sent=True)
                logger.info(f"Уведомление о заказе #{instance.id} успешно отправлено")
            
            # Выполняем отправку только после завершения текущей транзакции
            transaction.on_commit(send_and_update)
            
        except Exception as e:
            logger.error(f"Ошибка при подготовке или отправке уведомления для заказа #{instance.id}: {e}")