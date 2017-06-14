from django.db import models
from demandware.models import Category, ProductCategory, HeaderMgr
from django.core.exceptions import ValidationError

def insert_category(data=None, metadata=None):
	try:
		prd = Category(**data)
		pid = prd.save()
		return pid
	except ValidationError as e:
		return None

def get_cagetory(params=None):
	try:
		return Category.objects.get(**params)
	except Category.DoesNotExist as e:
		return None
	except Exception as e:
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
		return str(e)

def insert_product_category(data=None):
	from demandware.models import ProductMaster
	try:
		for item in data:
			values = dict(
				product=ProductMaster.objects.get(product_id=item['product_id']),
				category=Category.objects.get(category_id=item['category_id']),
			)
			ProductCategory.objects.update_or_create(**values)
		return None
	except Exception as e:
		print(str(e))
		return str(e)