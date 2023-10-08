# Generated by Django 4.2.5 on 2023-10-06 01:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_customuser_options_order_delivered'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supplier_orders', to='base.customuser', verbose_name='Yetkazib beruvchi'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_orders', to='base.customuser', verbose_name='Foydalanuvchi'),
        ),
    ]
