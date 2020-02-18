from django.contrib import admin
from .models import MarketplaceSource, ProductSearch


# Register your models here.
admin.site.register(MarketplaceSource)
admin.site.register(ProductSearch)