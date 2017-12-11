from django.db import models
from demandware.models import HeaderMgr

def insert_bulk_header(header_list=None, header_type=1):
	try:
		for item in header_list:
			values = dict(
				header_type=header_type,
				header_name=item,
			)
			HeaderMgr.objects.update_or_create(**values)
		return None
	except Exception as e:
		print(str(e))
		return str(e)
