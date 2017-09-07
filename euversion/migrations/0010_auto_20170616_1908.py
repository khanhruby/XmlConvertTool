# Generated by Django 2.0.dev20170604010711 on 2017-06-16 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demandware', '0009_auto_20170613_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_id',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='categorymeta',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='CategoryMeta_Category', to='demandware.Category', to_field='category_id'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ProductCategory_Category', to='demandware.Category', to_field='category_id'),
        ),
    ]
