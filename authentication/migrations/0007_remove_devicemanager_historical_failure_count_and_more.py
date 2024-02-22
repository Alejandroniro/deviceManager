# Generated by Django 5.0.2 on 2024-02-22 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_alter_devicemanager_execution_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicemanager',
            name='historical_failure_count',
        ),
        migrations.RemoveField(
            model_name='devicemanager',
            name='historical_success_count',
        ),
        migrations.RemoveField(
            model_name='devicemanager',
            name='total_failure_count',
        ),
        migrations.RemoveField(
            model_name='devicemanager',
            name='total_success_count',
        ),
        migrations.AddField(
            model_name='devicemanager',
            name='duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='devicemanager',
            name='execution_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='devicemanager',
            name='was_successful',
            field=models.CharField(max_length=255),
        ),
    ]