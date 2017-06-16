from django.db import models
from django.utils.timezone import now

# Create your models here.
class ProductMaster(models.Model):
	product_id = models.CharField(max_length=100, unique=True, default='') 
	season_code = models.CharField(max_length=100, default='')
	season_display_name = models.CharField(max_length=100, default='')
	brand_code = models.CharField(max_length=100, default='')
	brand_display_name = models.CharField(max_length=100, default='')
	display_name = models.CharField(max_length=255, default='')
	description = models.TextField(default='')
	functions = models.TextField(default='')
	online_shop_url = models.CharField(max_length=255, default='')
	product_commentary_1_image = models.CharField(max_length=255, default='')
	product_commentary_1_description = models.TextField(null=True)
	product_commentary_2_image = models.CharField(max_length=255, default='')
	product_commentary_2_description = models.TextField(null=True)
	product_commentary_3_image = models.CharField(max_length=255, default='')
	product_commentary_3_description = models.TextField(null=True)
	product_commentary_image_title = models.CharField(max_length=255, null=True)
	main_image = models.CharField(max_length=255, default='')
	del_flg = models.BooleanField(default=False)
	create_date = models.DateField(default=now, blank=True)
	update_date = models.DateField(auto_now=True, blank=True)

	def __str__(self):
		return str(self.product_id)

	class Meta:
		db_table = 'dtb_product_master'

	def get_variants(self):
		return Variant.objects.filter(product=self.product_id)

	def get_category(self):
		try:
			obj = ProductCategory.objects.get(product=self.product_id)
			if obj != None:
				return obj.category.category_name
			return ''
		except Exception as e:
			return ''


class ProductMeta(models.Model):
	product = models.ForeignKey(ProductMaster, on_delete=models.PROTECT, related_name='ProductMeta_ProductMaster', null=True, to_field='product_id')
	key = models.CharField(max_length=100, default='')
	value = models.TextField(null=True)

	def __str__(self):
		return str(self.product)

	class Meta:
		db_table = 'dtb_product_metadata'
		unique_together = ('product', 'key',)


class RelatedProduct(models.Model):
	product = models.ForeignKey(ProductMaster, on_delete=models.PROTECT, related_name='RelatedProduct_product_id', default='', to_field='product_id')
	related_product = models.ForeignKey(ProductMaster, on_delete=models.PROTECT, related_name='RelatedProduct_related_product_id', to_field='product_id')

	def __str__(self):
		return str(self.product)

	class Meta:
		db_table = 'dtb_related_product'


class Category(models.Model):
	category_id = models.CharField(max_length=100, unique=True, default='')
	category_parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='Category_CategoryParent', blank=True, null=True)
	category_name = models.CharField(max_length=100, default='')
	category_name_fr = models.CharField(max_length=100, null=True)
	category_name_jp = models.CharField(max_length=100, null=True)
	category_name_cn = models.CharField(max_length=100, null=True)
	category_level = models.IntegerField(default=0)
	del_flg = models.BooleanField(default=False)
	create_date = models.DateField(default=now, blank=True)
	update_date = models.DateField(auto_now=True, blank=True)

	def __str__(self):
		return str(self.category_id)

	class Meta:
		db_table = 'dtb_categories'
		unique_together = ('category_id', 'category_parent',)


class CategoryMeta(models.Model):
	category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='CategoryMeta_Category', null=True, to_field='category_id')
	key = models.CharField(max_length=100, default='')
	value = models.TextField(null=True)

	def __str__(self):
		return str(self.category)

	class Meta:
		db_table = 'dtb_category_metadata'
		unique_together = ('category', 'key',)


class ProductCategory(models.Model):
	product = models.ForeignKey(ProductMaster, on_delete=models.PROTECT, related_name='ProductCategory_ProductMaster', null=True, to_field='product_id')
	category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='ProductCategory_Category', null=True, to_field='category_id')

	def __str__(self):
		return str(self.product)

	class Meta:
		db_table = 'dtb_product_category'
		unique_together = ('product', 'category',)


class ProductImage(models.Model):
	product = models.ForeignKey(ProductMaster, on_delete=models.PROTECT, related_name='ProductImage_ProductMaster', null=True, to_field='product_id')
	color_code = models.CharField(max_length=10, default='')
	image_size = models.CharField(max_length=10, default='')
	product_image = models.CharField(max_length=255, default='')
	product_image_description = models.TextField(null=True)

	def __str__(self):
		return str(self.product)

	class Meta:
		db_table = 'dtb_product_image'


class Variant(models.Model):
	product = models.ForeignKey(ProductMaster, on_delete=models.PROTECT, related_name='Variant_ProductMaster', null=True, to_field='product_id')
	variation_jan = models.CharField(max_length=100, default='')
	country = models.CharField(max_length=50, default='')
	size_code = models.CharField(max_length=10, default='')
	size_display_name = models.CharField(max_length=100, default='')
	color_code = models.CharField(max_length=10, default='')
	color_display_name = models.CharField(max_length=100, default='')
	color_hexa_code = models.CharField(max_length=10, default='')
	price_amount = models.IntegerField(default=0)
	currency = models.CharField(max_length=10, default='')
	stock_quantity = models.IntegerField(default=1)
	del_flg = models.BooleanField(default=False)
	create_date = models.DateField(default=now, blank=True)
	update_date = models.DateField(blank=True, auto_now=True)

	def __str__(self):
		return str(self.product)

	class Meta:
		db_table = 'dtb_variant'

class HeaderMgr(models.Model):
	PRODUCT = 1
	CATEGORY = 2
	TYPE_CHOICES = (
		(PRODUCT, 'Product'),
		(CATEGORY, 'Category'),
	)
	header_type = models.SmallIntegerField(db_index=True, choices=TYPE_CHOICES, default=PRODUCT)
	header_name = models.CharField(max_length=50, default='')
	del_flg = models.BooleanField(default=False)

	class Meta:
		db_table = 'dtb_header_mgr'
