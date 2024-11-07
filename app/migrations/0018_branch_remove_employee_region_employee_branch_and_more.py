# Generated by Django 5.0.6 on 2024-11-07 12:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_employee_email_employee_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Branch Name')),
                ('registered_date_auto', models.DateTimeField(auto_now_add=True, verbose_name='Registered Date')),
            ],
            options={
                'verbose_name': 'Branch',
                'verbose_name_plural': 'Branch',
            },
        ),
        migrations.RemoveField(
            model_name='employee',
            name='region',
        ),
        migrations.AddField(
            model_name='employee',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.branch', verbose_name='Branch'),
        ),
        migrations.DeleteModel(
            name='Region',
        ),
    ]