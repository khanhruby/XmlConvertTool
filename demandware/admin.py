from django.contrib import admin
from .models import ProductMaster, ProductMeta, RelatedProduct, Category, CategoryMeta, Variant, ProductImage
from django.conf.urls import include, url
from django.http import HttpResponseBadRequest
from django.template.response import TemplateResponse
from django.shortcuts import render
from .views import import_action
from .forms import UploadFileForm
from .func.handle_uploaded import handle_uploaded_file
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
			# def choice_func(row):
			# 	q = Question.objects.filter(slug=row[0])[0]
			# 	row[0] = q
			# 	return row

			if form.is_valid():
				# request.FILES['myfile'].save_book_to_database(
				# 	models=[ProductMaster],
				# 	initializers=[None],
				# 	mapdicts=[
				# 		['product_id', 'season_code', 'season_display_name', 'brand_code', 'brand_display_name', 'display-name', 'description', 'functions', 'online_shop_pdp_url', 'product_commentary_1_image', 'product_commentary_1_description', 'product_commentary_2_image', 'product_commentary_2_description', 'product_commentary_3_image', 'product_commentary_3_description', 'product_commentary_image_title', 'main_image']
				# 	]
				# )
				handle_uploaded_file(form, request.FILES['myfile'])
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
