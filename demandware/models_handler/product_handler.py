from django.db import models
from demandware.models import ProductMaster, ProductMeta, ProductCategory, HeaderMgr, Variant
from django.core.exceptions import ValidationError
# Imports the Google Cloud client library
from google.cloud import translate
from django.conf import settings
# Instantiates a client
translate_client = translate.Client()

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
		data_extra = []
		for item in data:
			obj = None
			try:
				obj = ProductMaster.objects.get(product_id=item['product_id'])
				obj = update_multiple_fields(obj, item)
				obj.save()
			except ProductMaster.DoesNotExist:
				obj = ProductMaster(**item)
				obj.save()
			#Insert data extra
			if settings.MULTIPLE_LANGUAGE:
				insert_product_master_extra(obj, item)
		return None
	except Exception as e:
		return str(e)

def insert_product_master_extra(obj, data=None):
	if data == None: return;
	languages = settings.LANGEUAGE_MAPPING
	import json, re
	try:
		insert_default = dict(
			product_id=obj,
			country=data['country'],
			main_image=data['main_image'],
			functions=data['functions'],
			description=data['description'],
			display_name=data['display_name'],
			product_all_size_info=data['product_all_size_info'],
			product_all_color=data['product_all_color'],
			product_commentary_image_title=data['product_commentary_image_title'],
			product_commentary=data['product_commentary'],
		)
		insert_product_master_extra_language(data['country'].lower(), insert_default)
		### Insert auto translate
		# for lang in languages:
		# 	product_commentary = json.loads(data['product_commentary'])
		# 	# print(product_commentary)
		# 	for i in range(len(product_commentary)):
		# 		_items = list(product_commentary[i].items())
		# 		for key, value in _items:
		# 			_re_commentary = re.compile("product_commentary_(.*)_description")
		# 			_search_commentary = _re_commentary.search(key)
		# 			if _search_commentary != None:
		# 				product_commentary[i][key] = translate_client.translate(product_commentary[i][key], target_language=lang)['translatedText']
		# 	data['product_commentary'] = json.dumps(product_commentary)
		# 	item = dict(
		# 		product_id=obj,
		# 		country=lang,
		# 		main_image=data['main_image'],
		# 		functions=translate_client.translate(data['functions'], target_language=lang)['translatedText'],
		# 		description=translate_client.translate(data['description'], target_language=lang)['translatedText'],
		# 		display_name=translate_client.translate(data['display_name'], target_language=lang)['translatedText'],
		# 		product_all_size_info=data['product_all_size_info'],
		# 		product_all_color=data['product_all_color'],
		# 		product_commentary_image_title=translate_client.translate(data['product_commentary_image_title'], target_language=lang)['translatedText'],
		# 		product_commentary=translate_client.translate(data['product_commentary'], target_language=lang)['translatedText'],
		# 	)
		# 	insert_product_master_extra_language(lang, item)
	except Exception as e:
		print('[ERROR] Import Product Master Extra!', obj, str(e))
		return None

def insert_product_master_extra_language(lang, data=None):
	from demandware.models import ProductMaster_Extra
	try:
		prd_ex = ProductMaster_Extra.objects.get(product_id=data['product_id'], country=lang)
		prd_ex = update_multiple_fields(prd_ex, data)
		prd_ex.save()
	except ProductMaster_Extra.DoesNotExist:
		prd_ex = ProductMaster_Extra(**data)
		prd_ex.save()

def insert_related_product(data=None):
	from demandware.models import RelatedProduct
	try:
		errorList = []
		for item in data:
			print("[INSERT] ", item['product_id'], item['related_product_id'])
			listRelation = item['related_product_id'].split(",")
			for productIDRelation in listRelation:
				try:
					if item['product_id']==productIDRelation.strip():
						print("[SKIP] Source and target are the same!", item['product_id'], productIDRelation.strip())
						continue
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
					errorList.append("[SKIP] ProductMaster DoesNotExist: " + item['product_id'])
					print("[SKIP] ProductMaster DoesNotExist!", item['related_product_id'])
					continue
		return dict(
			message=errorList
		)
	except Exception as e:
		print(str(e))
		return str(e)

def insert_variant(data=None):
	try:
		errorList = []
		for item in data:
			try:
				print("[INSERT] ", item['product_id'], item['variation_jan'])
				item['product_id'] = ProductMaster.objects.get(product_id=item['product_id'])
				try:
					obj = Variant.objects.get(product_id=item['product_id'], variation_jan=item['variation_jan'])
					obj = update_multiple_fields(obj, item)
					obj.save()
				except Variant.DoesNotExist:
					obj = Variant(**item)
					obj.save()
			except ProductMaster.DoesNotExist:
				errorList.append("[SKIP] ProductMaster DoesNotExist: " + item['product_id'] + "/" + item['variation_jan'])
				print("[SKIP] ProductMaster DoesNotExist!", item['product_id'], item['variation_jan'])
				continue
		return dict(
			message=errorList
		)
	except Exception as e:
		print(str(e))
		return str(e)

def insert_product_image(data=None):
	from demandware.models import ProductImage
	try:
		errorList = []
		instances = []
		for item in data:
			try:
				productID = ProductMaster.objects.get(product_id=item['product_id'])
				# instances.append(ProductImage(**item))
				obj = ProductImage.objects.get(product_id=productID, color_code=item['color_code'], product_image=item['product_image'], image_size=item['image_size'])
				print("[DUP] ", item['product_id'], item['product_image'])
				errorList.append("[DUP] Image: " + item['product_id'] + '/' + item['product_image'])
			except ProductMaster.DoesNotExist:
				errorList.append("[SKIP] ProductMaster DoesNotExist: " + item['product_id'])
				print("[SKIP] ProductMaster DoesNotExist!", item['product_id'])
				continue
			except ProductImage.DoesNotExist:
				print("[INSERT] Image: ", item['product_id'], item['product_image'])
				item['product_id'] = ProductMaster.objects.get(product_id=item['product_id'])
				obj = ProductImage(**item)
				obj.save()
		# ProductImage.objects.bulk_create(instances, batch_size=None)
		return dict(
			message=errorList
		)
	except Exception as e:
		print(str(e))
		return str(e)

def get_product_master():
	products = ProductMaster.objects.all()
	# products = ProductMaster.objects.filter(product_id='QMCLJA13')
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
