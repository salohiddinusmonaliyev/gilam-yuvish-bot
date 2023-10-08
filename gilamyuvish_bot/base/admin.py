from django.contrib import admin

from .models import *

# Register your models here.
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'count', 'telegram_id')
    list_filter = ('full_name', 'count')
    search_fields = ('full_name', 'telegram_id')

class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'service', 'phone_number', 'price', 'is_completed')
    list_filter = ('user', 'price')
    search_fields = ('user__full_name', 'phone_number', 'service__name')


class ServiceModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_filter = ('name', 'price')
    search_fields = ('name', 'price')


admin.site.register(CustomUser, UserModelAdmin)
admin.site.register(Service, ServiceModelAdmin)
admin.site.register(Order, OrderModelAdmin)
admin.site.register(Invoice)
