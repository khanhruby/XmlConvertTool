from django import template

register = template.Library()

@register.filter(name='variantFilterCurrency')
def variantFilterCurrency(cur, currency):
	from demandware.models_handler.product_handler import get_variants_by_currency
	return get_variants_by_currency(currency)

@register.filter(name='filterImageGroups')
def filterImageGroups(imageGroupe):
	result = dict()
	for ig in imageGroupe:
		if ig.image_size not in result:
			result[ig.image_size] = []
		result[ig.image_size].append(ig)
	return result
