# Generated by Django 4.2.5 on 2025-03-10 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_remove_payment_payment_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='registration',
        ),
    ]
