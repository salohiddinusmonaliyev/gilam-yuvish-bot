from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class CustomUser(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="To'liq Ismi")
    telegram_id = models.BigIntegerField(null=True, unique=True, verbose_name="Telegram ID")
    count = models.BigIntegerField(null=True)

    # phone_number = models.BigIntegerField(null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Mijoz"
        verbose_name_plural = "Mijozlar"
        ordering = ['-count']


class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Xizmat Nomi")
    price = models.BigIntegerField(null=True, verbose_name="Xizmat Narxi")
    description = models.TextField(verbose_name="Xizmat Haqida")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Xizmatlar"
        verbose_name_plural = "Xizmatlar"


class Order(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, verbose_name="Foydalanuvchi",
                             related_name='user_orders')
    address = models.CharField(max_length=250, verbose_name="Manzil")
    service = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL, verbose_name="Xizmat turi")
    phone_number = models.CharField(max_length=250, null=True, verbose_name="Mijoz Telefon raqami")
    delivered = models.BooleanField(verbose_name="Yetkazib berildi", null=True)
    is_completed = models.BooleanField(verbose_name="Tugatildimi")
    supplier = models.ForeignKey(CustomUser, verbose_name="Yetkazib beruvchi", null=True, blank=True,
                                 on_delete=models.SET_NULL, related_name='supplier_orders')
    price = models.BigIntegerField(null=True, blank=True, default=0, verbose_name="Umumiy Narx")

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"

    def __str__(self):
        return f"{self.user.full_name} | {self.id}"


class Invoice(models.Model):
    order_number = models.BigIntegerField(null=True, unique=True)
    invoice = models.TextField()

    class Meta:
        verbose_name = "Nakladnoy"
        verbose_name_plural = "Nakladnoy"

