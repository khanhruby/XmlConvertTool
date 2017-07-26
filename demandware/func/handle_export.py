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
	if int(data_type) == 4:
		return handle_export_category()
	if int(data_type) == 5:
		return handle_export_product()
	if int(data_type) == 6:
		return handle_export_recommand()
	return None

def handle_export_catalogs():
	try:
		categories = get_categories()
		products = get_product_master()
		variants = get_product_variants()
		product_category = get_product_category()
		return dict(
			now=datetime.datetime.utcnow().isoformat() + "Z",
			categories=categories,
			productMaster=products,
			productVariants=variants,
			productCategory=product_category,
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

def handle_export_category():
	try:
		categories = get_categories()
		return dict(
			now=datetime.datetime.utcnow().isoformat() + "Z",
			categories=categories,
		)
	except Exception as e:
		return str(e)

def handle_export_product():
	try:
		products = get_product_master()
		variants = get_product_variants()
		product_category = get_product_category()
		return dict(
			now=datetime.datetime.utcnow().isoformat() + "Z",
			productMaster=products,
			productVariants=variants,
			productCategory=product_category,
		)
	except Exception as e:
		return str(e)

def handle_export_recommand():
	try:
		related_products = get_related_product()
		return dict(
			now=datetime.datetime.utcnow().isoformat() + "Z",
			relatedProducts=related_products,
		)
	except Exception as e:
		return str(e)
