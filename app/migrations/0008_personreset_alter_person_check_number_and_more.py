# Generated by Django 5.0.6 on 2024-09-28 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_delete_uramember_person_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonReset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_number', models.CharField(max_length=20)),
                ('image', models.FileField(upload_to='images/', verbose_name='Upload Ura mobile form')),
                ('simu', models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Phone number')),
                ('registered_date', models.DateField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
            },
        ),
        migrations.AlterField(
            model_name='person',
            name='check_number',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.FileField(default=1, upload_to='images/', verbose_name='Upload Ura mobile form'),
            preserve_default=False,
        ),
    ]
