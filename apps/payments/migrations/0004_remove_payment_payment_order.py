# Generated by Django 4.2.5 on 2025-03-10 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_alter_payment_confirmed_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='payment_order',
        ),
    ]
