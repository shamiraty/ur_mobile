# Generated by Django 5.0.6 on 2024-10-02 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_messagelog_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.FileField(default='images/no_image.jpg', upload_to='images/', verbose_name='Upload Ura mobile form'),
        ),
    ]
