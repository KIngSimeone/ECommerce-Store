from django.contrib import admin

from .models import (
                    UserAccount,
                    ManagerAccount,
                    ControllerAccount
                    )

admin.site.register(UserAccount)
admin.site.register(ManagerAccount)
admin.site.register(ControllerAccount)
