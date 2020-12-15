from django.contrib import admin

from .models import (
                    Business,
                    BusinessAddress,
                    BusinessLogo,
                    Product
)
admin.site.register(Business)
admin.site.register(BusinessAddress)
admin.site.register(BusinessLogo)
admin.site.register(Product)

