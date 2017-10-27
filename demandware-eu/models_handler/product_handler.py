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


def insert_bulk_product_master(data=None):
	try:
		instances = []
		for item in data:
			try:
				obj = ProductMaster.objects.get(product_id=item['product_id'])
				obj = update_multiple_fields(obj, item)
				obj.save()
			except ProductMaster.DoesNotExist:
				obj = ProductMaster(**item)
				obj.save()
		return None
	except Exception as e:
		return str(e)

def insert_related_product(data=None):
	from demandware.models import RelatedProduct
	try:
		for item in data:
			print(item['product_id'], item['related_product_id'])
			listRelation = item['related_product_id'].split(",")
			for productIDRelation in listRelation:
				try:
					productID = ProductMaster.objects.get(product_id=item['product_id'])
					relatedProductID = ProductMaster.objects.get(product_id=productIDRelation.strip())
					values = dict(
						product_id=productID,
						related_product_id=relatedProductID,
					)
					try:
						obj = RelatedProduct.objects.get(product_id=values['product_id'], related_product_id=values['related_product_id'])
					except RelatedProduct.DoesNotExist:
						obj = RelatedProduct(**values)
						obj.save()
				except ProductMaster.DoesNotExist:
					continue
		return None
	except Exception as e:
		print(str(e))
		return str(e)

def insert_variant(data=None):
	try:
		for item in data:
			try:
				print(item['product_id'], item['variation_jan'])
				item['product_id'] = ProductMaster.objects.get(product_id=item['product_id'])
				try:
					obj = Variant.objects.get(product_id=item['product_id'], variation_jan=item['variation_jan'])
					obj = update_multiple_fields(obj, item)
					obj.save()
				except Variant.DoesNotExist:
					obj = Variant(**item)
					obj.save()
			except ProductMaster.DoesNotExist:
				continue
		return None
	except Exception as e:
		print(str(e))
		return str(e)

def insert_product_image(data=None):
	from demandware.models import ProductImage
	try:
		instances = []
		for item in data:
			try:
				productID = ProductMaster.objects.get(product_id=item['product_id'])
				# instances.append(ProductImage(**item))
				obj = ProductImage.objects.get(product_id=productID, color_code=item['color_code'], product_image=item['product_image'], image_size=item['image_size'])
			except ProductMaster.DoesNotExist:
				print("ProductMaster DoesNotExist Skip: ", item['product_id'])
				continue
			except ProductImage.DoesNotExist:
				print("Insert Image: ", item['product_id'], item['product_image'])
				item['product_id'] = ProductMaster.objects.get(product_id=item['product_id'])
				obj = ProductImage(**item)
				obj.save()
		# ProductImage.objects.bulk_create(instances, batch_size=None)
		return None
	except Exception as e:
		print(str(e))
		return str(e)

def get_product_master():
	products = ProductMaster.objects.all()
	# products = ProductMaster.objects.filter(product_id='DAT-2722')
	return products

def get_product_variants():
	variants = Variant.objects.all().select_related("product_id")
	return variants

def get_list_currency():
	from django.db.models.aggregates import Count
	cur = Variant.objects.values('currency').annotate(counter=Count('currency')).all()
	# cur = Variant.objects.all().group_by('currency')
	return cur

def get_variants_by_currency(currency=None):
	return Variant.objects.filter(currency=currency)

def insert_product_metadata(data=None, extData=None):
	from demandware.models import ProductMeta
	try:
		for idx, items in zip(range(len(extData)), extData):
			_items = list(items.items())
			for key, value in _items:
				values = dict(
					product_id=ProductMaster.objects.get(product_id=data[idx]['product_id']),
					key=key,
					value=value,
				)
				try:
					obj = ProductMeta.objects.get(product_id=values['product_id'], key=key)
					obj.value = value
					obj.save()
				except ProductMeta.DoesNotExist:
					obj = ProductMeta(**values)
					obj.save()
	except Exception as e:
		raise e

def update_multiple_fields(obj, data=None):
	try:
		for (key, value) in data.items():
			setattr(obj, key, value)
		return obj
	except Exception as e:
		raise e

def get_product_category():
	products = ProductCategory.objects.all()
	return products

def get_related_product():
	from demandware.models import RelatedProduct
	related_products = RelatedProduct.objects.all()
	return related_products
