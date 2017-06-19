from django.db import models
from demandware.models import ProductMaster, ProductMeta, ProductCategory, HeaderMgr, Variant
from django.core.exceptions import ValidationError

def insert_product_master(data=None, metadata=None):
	try:
		prd = ProductMaster(**data)
		pid = prd.save()
		return pid
	except ValidationError as e:
		return None


def insert_bulk(data=None):
	try:
		instances = []
		for item in data:
			instances.append(ProductMaster(**item))
		ProductMaster.objects.bulk_create(instances, batch_size=None)
		return None
	except Exception as e:
		return str(e)

def insert_related_product(data=None):
	from demandware.models import RelatedProduct
	try:
		for item in data:
			values = dict(
				product=ProductMaster.objects.get(product_id=item['product_id']),
				related_product=ProductMaster.objects.get(product_id=item['related_product_id']),
			)
			RelatedProduct.objects.update_or_create(**values)
		return None
	except Exception as e:
		print(str(e))
		return str(e)

def insert_variant(data=None):
	try:
		instances = []
		for item in data:
			item['product'] = ProductMaster.objects.get(product_id=item['product_id'])
			del item['product_id']
			instances.append(Variant(**item))
		Variant.objects.bulk_create(instances, batch_size=None)
		return None
	except Exception as e:
		print(str(e))
		return str(e)

def insert_product_image(data=None):
	from demandware.models import ProductImage
	try:
		instances = []
		for item in data:
			item['product'] = ProductMaster.objects.get(product_id=item['product_id'])
			del item['product_id']
			instances.append(ProductImage(**item))
		ProductImage.objects.bulk_create(instances, batch_size=None)
		return None
	except Exception as e:
		print(str(e))
		return str(e)

def get_product_master():
	# products = ProductMaster.objects.all()
	products = ProductMaster.objects.filter(product_id='DSP-1700')
	return products

def get_product_variants():
	variants = Variant.objects.all().select_related("product")
	return variants

def get_list_currency():
	from django.db.models.aggregates import Count
	cur = Variant.objects.values('currency').annotate(counter=Count('currency')).all()
	# cur = Variant.objects.all().group_by('currency')
	return cur

def get_variants_by_currency(currency=None):
	return Variant.objects.filter(currency=currency)
