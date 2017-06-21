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

def handle_export(form=None):
	data_type = form.cleaned_data.get('data_type')
	if int(data_type) == 1:
		return handle_export_catalogs()
	if int(data_type) == 2:
		return handle_export_pricebook()
	if int(data_type) == 3:
		return handle_export_inventory()
	return None

def handle_export_catalogs():
	try:
		categories = get_categories()
		products = get_product_master()
		variants = get_product_variants()
		return dict(
			now=datetime.datetime.utcnow().isoformat() + "Z",
			categories=categories,
			productMaster=products,
			productVariants=variants,
		)
	except Exception as e:
		return str(e)

def handle_export_pricebook():
	try:
		list_cur = get_list_currency()
		return dict(
			now=datetime.datetime.utcnow().isoformat() + "Z",
			currencies=list_cur,
		)
	except Exception as e:
		return str(e)

def handle_export_inventory():
	try:
		variants = get_product_variants()
		return dict(
			now=datetime.datetime.utcnow().isoformat() + "Z",
			variants=variants,
		)
	except Exception as e:
		return str(e)
