# Generated by Django 4.2.4 on 2023-08-08 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='sir_name',
            new_name='middle_name_name',
        ),
    ]