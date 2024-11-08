# Generated by Django 5.0.6 on 2024-09-29 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_personreset_alter_person_check_number_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='personreset',
            options={'verbose_name': 'EmployeeReset', 'verbose_name_plural': 'EmployeesReset'},
        ),
        migrations.AlterField(
            model_name='personreset',
            name='simu',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Old / New Phone number'),
        ),
    ]
