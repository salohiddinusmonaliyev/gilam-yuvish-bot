# Generated by Django 4.2.5 on 2023-10-06 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_order_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='invoice',
            field=models.CharField(blank=True, null=True, verbose_name='Naklodnoy'),
        ),
    ]