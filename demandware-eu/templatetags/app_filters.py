from django import template
import datetime

register = template.Library()

@register.filter(name='variantFilterCurrency')
def variantFilterCurrency(cur, currency):
	from demandware.models_handler.product_handler import get_variants_by_currency
	return get_variants_by_currency(currency)

@register.filter(name='filterImageGroups')
def filterImageGroups(imageGroup):
	result = dict()
	for ig in imageGroup:
		if ig.image_size not in result:
			result[ig.image_size] = []
		result[ig.image_size].append(ig)
	return result

@register.filter(name='parseJSON')
def parseJSON(str):
	import json
	obj = json.loads(str)
	return obj


@register.filter(name='imageStringifyJSON')
def imageStringifyJSON(imageGroup):
	import json
	result = dict()
	for ig in imageGroup:
		if ig.image_size not in result:
			result[ig.image_size] = []
		result[ig.image_size].append(dict(
			image_path=ig.product_image,
			description=ig.product_image_description,
		))
	print(json.dumps(result))
	return json.dumps(result)

@register.filter(name='zlogger')
def zlogger(xstr):
	print(str(xstr) + ' ' + datetime.datetime.utcnow().isoformat() + "Z")
	return '';
