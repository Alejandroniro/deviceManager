# Generated by Django 5.0.2 on 2024-02-21 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_device_devicemanager_delete_customuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicemanager',
            name='historical_failure_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='devicemanager',
            name='historical_success_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='devicemanager',
            name='total_failure_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='devicemanager',
            name='total_success_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='devicemanager',
            name='was_successful',
            field=models.BooleanField(),
        ),
    ]
