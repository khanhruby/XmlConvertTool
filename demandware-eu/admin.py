from django.contrib import admin
# from django.contrib.admin.views.decorators import staff_member_required
from django.conf.urls import include, url
from django.http import HttpResponseBadRequest
from django.template.response import TemplateResponse
from django.shortcuts import render
from .forms import UploadFileForm, ExportForm
from .models import ProductMaster, ProductMeta, RelatedProduct, Category, CategoryMeta, Variant, ProductImage, HeaderMgr, ProductCategory
from demandware.func.handle_uploaded import handle_uploaded_file
from django.contrib import messages
import logging


# Get an instance of a logger
logger = logging.getLogger('django')

class CustomModelAdminMixin(object):

	def __init__(self, model, admin_site):
		self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
		super(CustomModelAdminMixin, self).__init__(model, admin_site)

	def get_urls(self):
		urls = super(CustomModelAdminMixin, self).get_urls()
		my_urls = [
			url(r'^add/$', self.import_view),
		]
		return my_urls + urls

	# def has_change_permission(self, request):
	# 	return False

	def import_view(self, request):
		model = self.model
		opts = model._meta
		result = dict()

		if request.method == 'POST' and 'myfile' in request.FILES:
			form = UploadFileForm(request.POST, request.FILES)
			if form.is_valid():
				res = handle_uploaded_file(form=form, f=request.FILES['myfile'], model_name=opts.model_name, model=model)
				if res['message'] != None:
					messages.error(request, res['message'])
				else:
					messages.success(request, 'Import success all! Inserted %d items' % res['count'])
			else:
				return HttpResponseBadRequest
		else:
			form = UploadFileForm()

		context = dict(
			self.admin_site.each_context(request),
			title=('Import %s') % opts.verbose_name,
			opts=opts,
			form=form,
			result=result,
		)

		return TemplateResponse(request, "admin/import.html", context)

class ProductMasterAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

class CategoryMetaAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

class ProductMetaAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

class RelatedProductAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

class CategoryAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

class VariantAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

class ProductImageAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

class ProductCategoryAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

# admin.site.register(CategoryMeta, CategoryMetaAdmin)
# admin.site.register(ProductMeta, ProductMetaAdmin)
admin.site.register(ProductMaster, ProductMasterAdmin)
admin.site.register(RelatedProduct, RelatedProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)

# @staff_member_required
def export_view(request):
	from .func.handle_export import handle_export
	import datetime

	if request.method == 'POST':
		form = ExportForm(request.POST)
		if form.is_valid():
			result = handle_export(form=form)
			if result != None:
				data_type = form.cleaned_data.get('data_type')
				_time = datetime.datetime.utcnow().isoformat() + "Z"
				response = None
				if int(data_type) == 1:
					response = TemplateResponse(request, "xmltemplate/catalog/main.xml", result, content_type='text/xml')
					response['Content-Disposition'] = 'attachment; filename=%s_%s.xml' % ('catalog', str(_time))
				if int(data_type) == 2:
					response =  TemplateResponse(request, "xmltemplate/pricebook/main.xml", result, content_type='text/xml')
					response['Content-Disposition'] = 'attachment; filename=%s_%s.xml' % ('pricebook', str(_time))
				if int(data_type) == 3:
					response = TemplateResponse(request, "xmltemplate/inventory/main.xml", result, content_type='text/xml')
					response['Content-Disposition'] = 'attachment; filename=%s_%s.xml' % ('inventory', str(_time))
				if int(data_type) == 4:
					response = TemplateResponse(request, "xmltemplate/catalog/main.xml", result, content_type='text/xml')
					response['Content-Disposition'] = 'attachment; filename=%s_%s.xml' % ('categories', str(_time))
				if int(data_type) == 5:
					response = TemplateResponse(request, "xmltemplate/catalog/main.xml", result, content_type='text/xml')
					response['Content-Disposition'] = 'attachment; filename=%s_%s.xml' % ('products', str(_time))
				if int(data_type) == 6:
					response = TemplateResponse(request, "xmltemplate/catalog/main.xml", result, content_type='text/xml')
					response['Content-Disposition'] = 'attachment; filename=%s_%s.xml' % ('recommand', str(_time))
				return response
			messages.error(request, result)
		else:
			return HttpResponseBadRequest
	else:
		form = ExportForm()
	context = dict(
		form=form,
	)
	return TemplateResponse(request, "admin/export.html", context)
