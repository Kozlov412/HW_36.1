# Generated by Django 5.2 on 2025-04-26 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='master',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='Активен'),
        ),
        migrations.AlterField(
            model_name='master',
            name='name',
            field=models.CharField(db_index=True, max_length=150, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('not_approved', 'Не подтвержден'), ('approved', 'Подтвержден'), ('in_progress', 'В процессе'), ('completed', 'Выполнен'), ('cancelled', 'Отменен')], db_index=True, default='not_approved', max_length=50, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='service',
            name='is_popular',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Популярная услуга'),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(db_index=True, max_length=200, verbose_name='Название'),
        ),
        migrations.AddIndex(
            model_name='master',
            index=models.Index(fields=['experience', 'is_active'], name='master_exp_active_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['status', 'appointment_date'], name='order_status_appt_idx'),
        ),
        migrations.AddIndex(
            model_name='service',
            index=models.Index(fields=['price', 'is_popular'], name='service_price_popular_idx'),
        ),
    ]
