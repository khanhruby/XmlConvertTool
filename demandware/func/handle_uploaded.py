from django.conf import settings
import pyexcel as pe
from demandware.models import ProductMaster, ProductMeta, RelatedProduct, Category, CategoryMeta, Variant, ProductImage
import logging

# Get an instance of a logger
logger = logging.getLogger('django')

def handle_uploaded_file(form, f):
	# params = f.get_params()
	# params.pop('file_content')
	# content = f.get_records(name_columns_by_row=1)

	# from_col=form.cleaned_data['from_col']
	# to_col=form.cleaned_data['to_col']
	# from_row=form.cleaned_data['from_row']
	# to_row=form.cleaned_data['to_row']
	# header_row=form.cleaned_data['header_row']

	"""
	- name_columns_by_row: start from -1
	- name_rows_by_column: start from 0
	"""
	dicts = f.get_dict(start_row=30, name_columns_by_row=-1, name_rows_by_column=0)
	# sheet = f.get_sheet(start_row=30)
	# sheet.name_columns_by_row(0)
	# sheet.name_rows_by_column(0)
	# content = []
	# for record in sheet:
	# 	content.append(record)
	# # session = Session()
	# f.save_to_database(
	# 	start_row=30,
	# 	name_rows_by_column=30,
	# 	model=ProductMaster,
	# 	mapdict=['product_id', 'season_code', 'season_display_name', 'brand_code', 'brand_display_name', 'display-name', 'description', 'functions', 'online_shop_pdp_url', 'product_commentary_1_image', 'product_commentary_1_description', 'product_commentary_2_image', 'product_commentary_2_description', 'product_commentary_3_image', 'product_commentary_3_description', 'product_commentary_image_title', 'main_image']
	# )
	pe.save_book_as(bookdict=dicts, dest_models=ProductMaster)
	# return content

# 前処理
def pretreatment(content, config):
	pass

def convert_letter_to_number(cn):
	# return ord(letter.lower()) - 96
	cn = cn.lower()
	return lambda cn: sum([((ord(cn[-1-pos]) - 64) * 26 ** pos) for pos in range(len(cn))])
