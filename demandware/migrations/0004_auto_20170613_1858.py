# Generated by Django 2.0.dev20170604010711 on 2017-06-13 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demandware', '0003_auto_20170613_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_parent',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
