# Generated by Django 4.2.5 on 2023-11-03 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.CharField(default='不詳', max_length=200),
        ),
    ]
