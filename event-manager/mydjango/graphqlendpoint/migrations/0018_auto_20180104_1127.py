# Generated by Django 2.0.1 on 2018-01-04 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('graphqlendpoint', '0017_call_current_agent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transfer',
            old_name='destination',
            new_name='tdestination',
        ),
        migrations.RenameField(
            model_name='transfer',
            old_name='origin',
            new_name='torigin',
        ),
        migrations.RenameField(
            model_name='transfer',
            old_name='timestamp',
            new_name='ttimestamp',
        ),
    ]
