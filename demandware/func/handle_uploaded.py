from django.conf import settings
from openpyxl import load_workbook
from openpyxl.utils import cell as pycell
from demandware.models import ProductMaster, ProductMeta, RelatedProduct, Category, CategoryMeta, Variant, ProductImage, HeaderMgr
import logging

# Get an instance of a logger
logger = logging.getLogger('django')

def handle_uploaded_file(form=None, f=None, model_name=None):
	wb = load_workbook(f, data_only=True)
	ws = wb.active
	min_row = form.cleaned_data.get('from_row')
	max_row = form.cleaned_data.get('to_row')
	min_col = form.cleaned_data.get('from_col')
	max_col = form.cleaned_data.get('to_col')
	header_row = form.cleaned_data.get('header_row')

	if max_row == 0:
		max_row = ws.max_row

	if max_col == '':
		max_col = ws.max_column

	logger.info(max_row)
	min_col_num = pycell.column_index_from_string(min_col)
	max_col_num = pycell.column_index_from_string(max_col)
	dataset = ws.iter_rows(min_row=min_row, min_col=min_col_num, max_col=max_col_num, max_row=max_row)

	header = ws.iter_rows(min_row=header_row, min_col=min_col_num, max_col=max_col_num, max_row=header_row)
	header = [cell.value for cell in list(header)[0]]

	_count = 0
	insertDataSet = []
	for row in dataset:
		values = {}
		for key, _cell in zip(header, row):
			values[key] = _cell.value if _cell.value else ''
		_count = _count + 1
		insertDataSet.append(values)
	
	message = detect_service(model_name=model_name, data=insertDataSet, header=header)
	result = dict(
		message=message,
		count=_count
	)
	return result


def detect_service(model_name=None, data=None, header=None):
	print(model_name)
	if model_name == 'productmaster':
		return product_master_process(data=data, header=header)

	if model_name == 'relatedproduct':
		return related_product_process(data=data)

	if model_name == 'variant':
		return variant_process(data=data)

	if model_name == 'productimage':
		return product_image_process(data=data)

	if model_name == 'category':
		return category_process(data=data, header=header)

	if model_name == 'productcategory':
		return product_category_process(data=data)

	return None


def get_model_fields(model):
    return [f.name for f in model._meta.fields]


def product_master_process(data=None, header=None):
	"""
	1. Insert header to header_mgr db
	2. If header name is existing in table, then insert to table
		Else insert or update to metadata
	"""
	from demandware.models_handler.header_handler import insert_bulk as header_insert_all
	from demandware.models_handler.product_handler import insert_product_master, insert_bulk
	result = None

	### Insert header data
	result = header_insert_all(header_list=header, header_type=HeaderMgr.PRODUCT)

	### Insert data
	result = insert_bulk(data=data)
	return result

def related_product_process(data=None):
	from demandware.models_handler.product_handler import insert_related_product
	return insert_related_product(data)

def variant_process(data=None):
	from demandware.models_handler.product_handler import insert_variant
	return insert_variant(data)

def product_image_process(data=None):
	from demandware.models_handler.product_handler import insert_product_image
	return insert_product_image(data)

def category_process(data=None, header=None):
	from demandware.models_handler.header_handler import insert_bulk as header_insert_all
	from demandware.models_handler.category_handler import insert_bulk

	### Insert header data
	result = header_insert_all(header_list=header, header_type=HeaderMgr.CATEGORY)

	### Insert data
	result = insert_bulk(data=data)
	return result

def product_category_process(data=None):
	from demandware.models_handler.category_handler import insert_product_category
	return insert_product_category(data)
