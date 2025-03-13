# Generated by Django 4.2.5 on 2025-03-13 02:01

import apps.users.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_delete_clickorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='certificates',
            field=models.FileField(null=True, upload_to=apps.users.models.user_directory_path),
        ),
        migrations.AddField(
            model_name='applicant',
            name='exam_date',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.examdate'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='program',
            name='exam_date',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.examdate'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='examregistration',
            name='status',
            field=models.CharField(choices=[('pending_payment', 'Ожидание платежа'), ('confirmed', 'Оплачено'), ('failed', 'Провален'), ('canceled', 'Отменено')], default='pending_payment', max_length=20),
        ),
    ]
