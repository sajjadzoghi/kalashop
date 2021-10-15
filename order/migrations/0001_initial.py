# Generated by Django 3.2.5 on 2021-10-15 04:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ')),
                ('total_price', models.IntegerField(verbose_name='مبلغ کل سفارش (بدون احتساب تخفیف)')),
                ('discount', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100)], verbose_name='درصد تخفیف')),
                ('shipping', models.CharField(choices=[('پیشتاز', 'پیشتاز'), ('سفارشی', 'سفارشی')], default='سفارشی', max_length=20, verbose_name='نوع پست')),
                ('status', models.CharField(choices=[('انصراف', 'انصراف'), ('فعال', 'فعال'), ('بارگیری', 'پرداخت موفق و درحال بارگیری از انبار'), ('پیک', 'درحال ارسال توسط پیک'), ('تحویل', 'تحویل سفارش به مشتری')], default='بارگیری', max_length=20, verbose_name='وضعیت')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='orders', to='accounts.address', verbose_name='آدرس')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'سفارش',
                'verbose_name_plural': 'سفارش\u200cها',
                'ordering': ['datetime'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='تعداد')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.order', verbose_name='سفارش')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='product.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'آیتم سفارش',
                'verbose_name_plural': 'آیتم\u200cهای سفارش',
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15, verbose_name='کد تخفیف')),
                ('amount', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100)], verbose_name='درصد تخفیف')),
                ('expire_date', models.DateField(blank=True, null=True, verbose_name='تاریخ انقضاء')),
                ('customers', models.ManyToManyField(related_name='coupons', to=settings.AUTH_USER_MODEL, verbose_name='کاربران موردنظر')),
            ],
            options={
                'verbose_name': 'کد تخفیف',
                'verbose_name_plural': 'کدهای تخفیف',
            },
        ),
    ]
