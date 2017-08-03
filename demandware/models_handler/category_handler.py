from django.db import models
from demandware.models import Category, ProductCategory, HeaderMgr
from django.core.exceptions import ValidationError
import logging

# Get an instance of a logger
logger = logging.getLogger('django')

def insert_category(data=None, metadata=None):
	result = dict(
		error=None,
		obj=None
	)
	try:
		print(data['category_id'])
		obj = Category.objects.get(category_id=data['category_id'])
		obj = update_multiple_fields(obj, data)
		obj.save()
		result['obj'] = obj
		return result
	except Category.DoesNotExist:
		obj = Category(**data)
		obj.save()
		result['obj'] = obj
		return result
	except ValidationError as e:
		result['error'] = str(e)
		return result

def get_cagetory(params=None):
	try:
		return Category.objects.get(**params)
	except Category.DoesNotExist as e:
		return None
	except Exception as e:
		logger.info(str(e))
		raise e

def insert_bulk(data=None):
	try:
		instances = []
		for item in data:
			if item['category_parent'] != None or item['category_parent'] != '':
				cat = get_cagetory({'category_id':item['category_parent']})
				item['category_parent_id'] = cat.id if cat != None else None
			else:
				item['category_parent_id'] = None
			item['category_level'] = int(item['category_level'])
			del item['category_parent']
			Category.objects.update_or_create(**item)
		return None
	except Exception as e:
		print(str(e))
		logger.info(str(e))
		return str(e)

def insert_product_category(data=None):
	from demandware.models import ProductMaster
	try:
		for item in data:
			print(item['product_id'], item['category_id'])
			values = dict(
				product_id=ProductMaster.objects.get(product_id=item['product_id']),
				category_id=Category.objects.get(category_id=item['category_id']),
			)
			ProductCategory.objects.update_or_create(**values)
		return None
	except Exception as e:
		print(str(e))
		logger.info(str(e))
		return str(e)

def get_categories(_category_parent_=None):
	categories = Category.objects.all().select_related("category_parent")
	return categories

def update_multiple_fields(obj, data=None):
	try:
		for (key, value) in data.items():
			setattr(obj, key, value)
		return obj
	except Exception as e:
		raise e
