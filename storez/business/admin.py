from django.contrib import admin

from .models import (
                    Business,
                    BusinessAddress,
                    Photo,
                    Product
)
admin.site.register(Business)
admin.site.register(BusinessAddress)
admin.site.register(Photo)
admin.site.register(Product)

