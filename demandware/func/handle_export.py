"""
Check xml schema: https://pypi.python.org/pypi/xmlschema/0.9.8
"""
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.conf import settings
from django import template
from demandware.models import ProductMaster, ProductMeta, RelatedProduct, Category, CategoryMeta, Variant, ProductImage, HeaderMgr
from demandware.models_handler.category_handler import get_categories
from demandware.models_handler.product_handler import *
import datetime
import xmlschema
import logging

# Get an instance of a logger
logger = logging.getLogger('django')

register = template.Library()

def handle_export(form=None):
	data_type = form.cleaned_data.get('data_type')
	if int(data_type) == 1:
		return handle_export_catalogs()
	return None

def handle_export_catalogs():
	try:
		categories = get_categories()
		products = get_product_master()
		variants = get_product_variants()
		print(products[0].get_variants())
		return dict(
			now=datetime.datetime.utcnow().isoformat() + "Z",
			categories=categories,
			productMaster=products,
			productVariants=variants,
		)
		pass
	except Exception as e:
		raise e

@register.simple_tag
def get_product_variants(product_id=None):
	return [dict(test=1),dict(test=2),]

# def validate(xml_path: str, xsd_path: str) -> bool:
# 	from lxml import etree
# 	try:
# 		xmlschema_doc = etree.parse(xsd_path)
# 		xmlschema = etree.XMLSchema(xmlschema_doc)

# 		xml_content = render(None, 'xmltemplate/catalog/catalog.xml', {"foo": "bar"}, content_type="application/xhtml+xml")
# 		xml_doc = etree.parse(xml_content)
# 		result = xmlschema.validate(xml_doc)


# 		# xs = xmlschema.XMLSchema('demandware/templates/xmlschema/catalog.xsd')
# 		# xml_content = render(None, 'xmltemplate/catalog/catalog.xml', {"foo": "bar"}, content_type="application/xhtml+xml")
# 		# valid = xs.validate(xml_content)

# 		return result
# 	except Exception as e:
# 		raise e