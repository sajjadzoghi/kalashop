# Generated by Django 3.2.5 on 2021-09-10 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'سفارش', 'verbose_name_plural': 'سفارش\u200cها'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'محصول در یک سفارش', 'verbose_name_plural': 'محصولات هر سفارش'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'پرداخت', 'verbose_name_plural': 'پرداخت\u200cها'},
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='payment_status',
            new_name='status',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_num',
        ),
    ]