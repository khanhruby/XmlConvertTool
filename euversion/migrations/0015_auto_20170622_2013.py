# Generated by Django 2.0.dev20170604010711 on 2017-06-22 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demandware', '0014_auto_20170622_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorymeta',
            name='category_id',
            field=models.ForeignKey(db_column='category_id', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='CategoryMeta_Category', to='demandware.Category', to_field='category_id'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='category_id',
            field=models.ForeignKey(db_column='category_id', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ProductCategory_Category', to='demandware.Category', to_field='category_id'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='product_id',
            field=models.ForeignKey(db_column='product_id', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ProductCategory_ProductMaster', to='demandware.ProductMaster', to_field='product_id'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product_id',
            field=models.ForeignKey(db_column='product_id', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ProductImage_ProductMaster', to='demandware.ProductMaster', to_field='product_id'),
        ),
        migrations.AlterField(
            model_name='productmeta',
            name='product_id',
            field=models.ForeignKey(db_column='product_id', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ProductMeta_ProductMaster', to='demandware.ProductMaster', to_field='product_id'),
        ),
        migrations.AlterField(
            model_name='relatedproduct',
            name='product_id',
            field=models.ForeignKey(db_column='product_id', default='', on_delete=django.db.models.deletion.PROTECT, related_name='RelatedProduct_product_id', to='demandware.ProductMaster', to_field='product_id'),
        ),
        migrations.AlterField(
            model_name='relatedproduct',
            name='related_product_id',
            field=models.ForeignKey(db_column='related_product_id', on_delete=django.db.models.deletion.PROTECT, related_name='RelatedProduct_related_product_id', to='demandware.ProductMaster', to_field='product_id'),
        ),
        migrations.AlterField(
            model_name='variant',
            name='product_id',
            field=models.ForeignKey(db_column='product_id', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Variant_ProductMaster', to='demandware.ProductMaster', to_field='product_id'),
        ),
    ]
