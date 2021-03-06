from django import template
import sys
import datetime
import cgi
import re
from collections import OrderedDict
from django.conf import settings

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

@register.filter(name='filterImageDetailCut1')
def filterImageDetailCut1(imageGroup):
	detailcut1 = []
	result = OrderedDict()
	for ig in imageGroup:
		if ig.image_size == 'detailcut1':
			detailcut1.append(ig.product_image)
	
	for item in detailcut1:
		_re_commentary = re.compile("(.*)_(.*)_detailcut1_(0[1-9]|1[0]).(.*)")
		_search_commentary = _re_commentary.search(item)
		if _search_commentary != None:
			result[_search_commentary.group(3)] = _search_commentary.group(0)
	for idx in range(1,11):
		if str(idx).zfill(2) not in result:
			result[str(idx).zfill(2)] = ''
	return result

@register.filter(name='filterImageDetailCut2')
def filterImageDetailCut2(imageGroup):
	detailcut2 = []
	result = OrderedDict()
	for ig in imageGroup:
		if ig.image_size == 'detailcut2':
			detailcut2.append(ig.product_image)
	
	for item in detailcut2:
		_re_commentary = re.compile("(.*)_(.*)_detailcut2_(0[1-9]|1[0]).(.*)")
		_search_commentary = _re_commentary.search(item)
		if _search_commentary != None:
			result[int(_search_commentary.group(3))] = _search_commentary.group(0)
	for idx in range(1,4):
		if idx not in result:
			result[idx] = ''
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

@register.filter(name='ztrim')
def ztrim(xstr):
	return str(xstr).strip()

@register.tag(name='set')
def set_var(parser, token):
	"""
	{% set some_var = '123' %}
	"""
	parts = token.split_contents()
	if len(parts) < 4:
		raise template.TemplateSyntaxError("'set' tag must be of the form: {% set <var_name> = <var_value> %}")

	return SetVarNode(parts[1], parts[3])

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

@register.simple_tag(name='printProductAttr')
def printProductAttr(tag_name, data, *args):
	try:
		_format = '<{0} xml:lang="{1}" {3}>{2}</{0}>'
		result = ''
		if(type(data) is dict):
			result += _format.format(tag_name, 'x-default', cgi.escape(str(getattr(data['en'], args[0]))), args[1] if len(args) > 1 else '') + '\n'
		else:
			result += _format.format(tag_name, 'x-default', cgi.escape(str(data)), args[0]) + '\n'
		
		for lang in settings.LANGEUAGE_MAPPING:
			if(type(data) is dict):
				result += _format.format(tag_name, settings.LANGEUAGE_MAPPING[lang], cgi.escape(str(getattr(data[lang.lower()], args[0]))), args[1] if len(args) > 1 else '') + '\n'
			else:
				result += _format.format(tag_name, settings.LANGEUAGE_MAPPING[lang], cgi.escape(str(data)), args[0]) + '\n'
		return result
	except Exception as e:
		print('Skip Error!')

@register.simple_tag(name='printJSonAttr')
def printJSonAttr(tag_name, data, *args):
	try:
		import json
		_format = '<{0} xml:lang="{1}" attribute-id="{3}">{2}</{0}>'
		result = ''
		default_obj = json.loads(cgi.escape(str(getattr(data['en'], args[0]))))
		
		for item in default_obj:
			for key, value in item.items():
				result += _format.format(tag_name, settings.LANGEUAGE_MAPPING['en'], cgi.escape(str(value)), key) + '\n'

		for lang in settings.LANGEUAGE_MAPPING:
			obj = json.loads(cgi.escape(str(getattr(data[lang.lower()], args[0]))))
			for item in obj:
				for key, value in item.items():
					result += _format.format(tag_name, settings.LANGEUAGE_MAPPING[lang], cgi.escape(str(value)), key) + '\n'
		return result
	except Exception as e:
		print('Skip Error!')

register.filter("call", callMethod)
register.filter("args", args)
