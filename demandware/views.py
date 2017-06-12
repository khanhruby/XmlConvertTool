from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse


# Create your views here.
def index(request):
	return HttpResponse("Hello, world. You're at the Demandware index.")

def import_action(self, request):
# 	model = self.model
# 	opts = model._meta
# 	context = dict(
# 		self.admin_site.each_context(request),
# 		title=('Import %s') % opts.verbose_name,
# 		# Anything else you want in the context...
# 		data={
# 			'key': "Import Content"
# 		},
# 		opts = opts,
# 	)
# 	return render(request, "admin/import.html", context)
	pass