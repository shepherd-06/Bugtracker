# Generated by Django 2.2.4 on 2019-09-24 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('token_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecttoken',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='projecttoken',
            name='last_access',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='projecttoken',
            name='refresh_token',
            field=models.CharField(max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='projecttoken',
            name='token',
            field=models.CharField(max_length=36, unique=True),
        ),
    ]
