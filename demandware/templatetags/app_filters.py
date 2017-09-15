from django import template
import datetime

register = template.Library()

class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value

        return u""

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
	return ''

@register.filter(name='set_var')
def set_var(key, value):
    return value

# @register.filter(name='getProductDataByLang')
# def getProductDataByLang(lang):
#     return self.

# {% call_method obj_customer 'get_something' obj_business %}
@register.simple_tag(name='call_method')
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)

# {{ meeting|args:arg1|args:arg2|call:"getPrice" }}
def callMethod(obj, methodName):
	method = getattr(obj, methodName)

	if obj.__dict__.has_key("__callArg"):
		ret = method(*obj.__callArg)
		del obj.__callArg
		return ret
	return method()
 
def args(obj, arg):
	if not obj.__dict__.has_key("__callArg"):
		obj.__callArg = []

	obj.__callArg += [arg]
	return obj
 
register.filter("call", callMethod)
register.filter("args", args)


# 
