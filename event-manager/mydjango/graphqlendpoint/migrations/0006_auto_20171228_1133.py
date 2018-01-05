# Generated by Django 2.0 on 2017-12-28 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('graphqlendpoint', '0005_auto_20171228_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='primaryagent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='calls', to='graphqlendpoint.Agent_unify'),
        ),
        migrations.AlterField(
            model_name='call',
            name='secondaryagent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='calls_alt', to='graphqlendpoint.Agent_unify'),
        ),
    ]
