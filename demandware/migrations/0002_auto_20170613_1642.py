# Generated by Django 2.0.dev20170604010711 on 2017-06-13 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demandware', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='relatedproduct',
            old_name='related_product',
            new_name='related_product_id',
        ),
    ]