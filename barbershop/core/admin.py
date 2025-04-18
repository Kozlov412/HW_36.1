from django.contrib import admin

from django.contrib import admin
from .models import Service, Master, Order, Review

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration', 'is_popular']
    list_filter = ['is_popular']
    search_fields = ['name', 'description']

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'experience', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'phone', 'address']
    filter_horizontal = ['services']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client_name', 'phone', 'master', 'status', 'appointment_date', 'date_created']
    list_filter = ['status', 'master']
    search_fields = ['client_name', 'phone', 'comment']
    filter_horizontal = ['services']
    readonly_fields = ['date_created', 'date_updated']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'master', 'rating', 'created_at', 'is_published']
    list_filter = ['rating', 'is_published', 'master']
    search_fields = ['client_name', 'text']
    readonly_fields = ['created_at']