# Generated by Django 2.0.dev20170604010711 on 2017-09-07 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demandware', '0017_remove_productmaster_model_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_custom_url',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='category',
            name='category_position',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='productmaster',
            name='No',
            field=models.IntegerField(default=0),
        ),
    ]
