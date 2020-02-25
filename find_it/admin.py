from django.contrib import admin
from .models import MarketplaceSource, ProductSearch

admin.site.site_header = 'Find It Administration'

# Register your models here.
admin.site.register(MarketplaceSource)
admin.site.register(ProductSearch)