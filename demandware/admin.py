from django.contrib import admin
from .models import ProductMaster, ProductMeta, RelatedProduct, Category, CategoryMeta, Variant, ProductImage, HeaderMgr, ProductCategory
from django.conf.urls import include, url
from django.http import HttpResponseBadRequest
from django.template.response import TemplateResponse
from django.shortcuts import render
from .views import import_action
from .forms import UploadFileForm
from .func.handle_uploaded import handle_uploaded_file
from django.contrib import messages
import logging


# Get an instance of a logger
logger = logging.getLogger('django')

# Register your models here.
class ProductMasterAdmin(admin.ModelAdmin):
	def import_product(self, request, queryset):
		pass

	def has_add_permission(self, request):
		return False

@admin.register(CategoryMeta)
@admin.register(ProductMeta)
@admin.register(RelatedProduct)
@admin.register(Category)
@admin.register(Variant)
@admin.register(ProductImage)
@admin.register(ProductMaster)
@admin.register(ProductCategory)
class disableAction(admin.ModelAdmin):
	def get_urls(self):
		urls = super(disableAction, self).get_urls()
		my_urls = [
			url(r'^add/$', self.import_view),
		]
		return my_urls + urls

	def has_change_permission(self, request):
		return False

	def import_view(self, request):
		model = self.model
		opts = model._meta
		result = dict()

		if request.method == 'POST' and 'myfile' in request.FILES:
			form = UploadFileForm(request.POST, request.FILES)
			if form.is_valid():
				res = handle_uploaded_file(form=form, f=request.FILES['myfile'], model_name=opts.model_name)
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
