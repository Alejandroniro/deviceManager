# Generated by Django 5.0.2 on 2024-02-22 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_remove_devicemanager_historical_failure_count_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicemanager',
            name='duration',
        ),
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
            name='execution_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='devicemanager',
            name='was_successful',
            field=models.BooleanField(),
        ),
    ]